// Polyglot frontend — no login, no accounts. Just paste code and identify.
const LANGUAGES = ["C", "C#", "C++", "Go", "Java", "JavaScript", "PHP", "Python", "Rust", "TypeScript"];
const $ = (id) => document.getElementById(id);

async function api(path, opts) {
  const res = await fetch(path, opts);
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.detail || ("HTTP " + res.status));
  return data;
}

// ---------- tabs ----------
document.querySelectorAll(".tab").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach((b) => b.classList.remove("active"));
    document.querySelectorAll(".panel").forEach((p) => p.classList.remove("active"));
    btn.classList.add("active");
    $("tab-" + btn.dataset.tab).classList.add("active");
    if (btn.dataset.tab === "arena") loadArena();
    if (btn.dataset.tab === "length") loadLength();
    if (btn.dataset.tab === "dataset") loadDataset();
  });
});

// ---------- editor: gutter + meta ----------
const codeInput = $("codeInput");
const gutter = $("gutter");
function syncEditor() {
  const lines = codeInput.value.split("\n").length;
  gutter.textContent = Array.from({ length: lines }, (_, i) => i + 1).join("\n");
  const chars = codeInput.value.length;
  $("lenMeta").textContent = `${lines} line${lines === 1 ? "" : "s"} · ${chars} chars`;
}
codeInput.addEventListener("input", syncEditor);
codeInput.addEventListener("scroll", () => { gutter.scrollTop = codeInput.scrollTop; });
codeInput.addEventListener("keydown", (e) => {
  if (e.key === "Tab") {
    e.preventDefault();
    const s = codeInput.selectionStart;
    codeInput.value = codeInput.value.slice(0, s) + "    " + codeInput.value.slice(codeInput.selectionEnd);
    codeInput.selectionStart = codeInput.selectionEnd = s + 4;
    syncEditor();
  }
});
syncEditor();

// ---------- sample chips ----------
const chips = $("sampleChips");
LANGUAGES.forEach((lang) => {
  const b = document.createElement("button");
  b.className = "chip";
  b.textContent = lang;
  b.addEventListener("click", async () => {
    b.textContent = lang + " …";
    try {
      const d = await api(`/api/samples/${encodeURIComponent(lang)}`);
      codeInput.value = d.sample;
      syncEditor();
    } catch (e) { alert(e.message); }
    b.textContent = lang;
  });
  chips.appendChild(b);
});

$("clearBtn").addEventListener("click", () => {
  codeInput.value = "";
  syncEditor();
  $("resultEmpty").hidden = false;
  $("resultBody").hidden = true;
});

// ---------- identify ----------
$("identifyBtn").addEventListener("click", async () => {
  const code = codeInput.value;
  if (code.trim().length < 3) { alert("Paste a code snippet first."); return; }
  const btn = $("identifyBtn");
  btn.textContent = "⏳ Identifying…";
  btn.disabled = true;
  try {
    const r = await api("/api/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code }),
    });
    $("resultEmpty").hidden = true;
    $("resultBody").hidden = false;
    $("predLang").textContent = r.language;
    $("predConf").textContent = (r.confidence * 100).toFixed(1) + "% confident";
    $("confFill").style.width = Math.max(4, r.confidence * 100) + "%";
    const agreeCount = r.votes[r.language] || 0;
    $("agreeLine").textContent = agreeCount === 3
      ? "✓ All 3 models agree"
      : `⚠ ${agreeCount}/3 models agree — closest call`;
    $("top3").innerHTML = r.top3.map((t, i) => `
      <div class="bar-row ${i === 0 ? "top" : ""}">
        <span>${t.language}</span>
        <div class="bar-track"><div class="bar-fill" style="width:${(t.probability * 100).toFixed(1)}%"></div></div>
        <span>${(t.probability * 100).toFixed(1)}%</span>
      </div>`).join("");
    $("votes").innerHTML = Object.entries(r.models).map(([name, m]) => `
      <div class="vote-row"><span>${name}</span><span class="v-lang">${m.language} · ${(m.confidence * 100).toFixed(1)}%</span></div>`).join("");
    $("lenChip").innerHTML = `Snippet length: <b>${r.length.lines} lines · ${r.length.chars} chars</b> — bucket: <b>${r.length.bucket}</b>`;
  } catch (e) { alert(e.message); }
  btn.textContent = "▶ Identify Language";
  btn.disabled = false;
});

// ---------- health ----------
api("/api/health").then((h) => {
  $("healthLine").textContent = `${h.snippets} snippets · ${h.models.length} models loaded`;
}).catch(() => { $("healthLine").textContent = "server offline"; });

// ---------- model arena ----------
let evalCache = null;
async function getEval() {
  if (!evalCache) evalCache = await api("/api/evaluate");
  return evalCache;
}
async function loadArena() {
  const ev = await getEval();
  const cards = $("modelCards");
  cards.innerHTML = Object.entries(ev.models).map(([name, m]) => `
    <div class="mcard ${name === ev.best_model ? "best" : ""}">
      ${name === ev.best_model ? '<span class="badge">★ BEST</span>' : ""}
      <h3>${name}</h3>
      <div class="big-acc">${(m.accuracy * 100).toFixed(1)}%</div>
      <div class="metrics">
        precision <b>${(m.precision * 100).toFixed(1)}%</b> ·
        recall <b>${(m.recall * 100).toFixed(1)}%</b> ·
        F1 <b>${(m.f1 * 100).toFixed(1)}%</b><br>
        test set: <b>${m.test_size} snippets</b>
      </div>
    </div>`).join("");
  $("compareTable").innerHTML = `
    <tr><th>Model</th><th class="num">Accuracy</th><th class="num">Precision</th><th class="num">Recall</th><th class="num">F1</th></tr>
    ${Object.entries(ev.models).sort((a, b) => b[1].accuracy - a[1].accuracy).map(([name, m]) => `
      <tr><td>${name}${name === ev.best_model ? " ★" : ""}</td>
      <td class="num">${(m.accuracy * 100).toFixed(1)}%</td>
      <td class="num">${(m.precision * 100).toFixed(1)}%</td>
      <td class="num">${(m.recall * 100).toFixed(1)}%</td>
      <td class="num">${(m.f1 * 100).toFixed(1)}%</td></tr>`).join("")}`;
  $("cmModel").textContent = `— ${ev.best_model}`;
  const labels = ev.labels;
  let html = `<table class="cm"><tr><th>true ↓ / pred →</th>${labels.map((l) => `<th>${l}</th>`).join("")}</tr>`;
  ev.confusion_matrix.forEach((row, i) => {
    html += `<tr><th>${labels[i]}</th>` + row.map((v, j) => {
      const cls = i === j ? "diag" : (v > 0 ? "off" : "");
      return `<td class="${cls}">${v}</td>`;
    }).join("") + "</tr>";
  });
  $("cmWrap").innerHTML = html + "</table>";
}

// ---------- length lab ----------
const BUCKET_COLORS = { short: "#58a6ff", medium: "#3fb950", long: "#d29922" };
async function loadLength() {
  const ev = await getEval();
  const chart = $("lengthChart");
  chart.innerHTML = Object.entries(ev.by_length).map(([name, buckets]) => `
    <div class="lchart-row"><span>${name}</span><div class="lchart-bars">
      ${["short", "medium", "long"].map((b) => {
        const v = buckets[b];
        return v ? `<div class="lbar"><div class="fill" style="width:${(v.accuracy * 120).toFixed(0)}px;background:${BUCKET_COLORS[b]}"></div><span>${b} ${(v.accuracy * 100).toFixed(0)}%</span></div>` : "";
      }).join("")}
    </div></div>`).join("");
  $("lengthTable").innerHTML = `
    <tr><th>Model</th><th class="num">Short (1–3 lines)</th><th class="num">Medium (4–10)</th><th class="num">Long (11+)</th></tr>
    ${Object.entries(ev.by_length).map(([name, b]) => `
      <tr><td>${name}</td>
      <td class="num">${b.short ? (b.short.accuracy * 100).toFixed(1) + "% (n=" + b.short.n + ")" : "—"}</td>
      <td class="num">${b.medium ? (b.medium.accuracy * 100).toFixed(1) + "% (n=" + b.medium.n + ")" : "—"}</td>
      <td class="num">${b.long ? (b.long.accuracy * 100).toFixed(1) + "% (n=" + b.long.n + ")" : "—"}</td></tr>`).join("")}`;
}

// ---------- dataset ----------
function fillLangSelects(langs) {
  ["browseLang", "addLang"].forEach((id) => {
    $(id).innerHTML = langs.map((l) => `<option value="${l}">${l}</option>`).join("");
  });
}
async function loadDataset() {
  const stats = await api("/api/dataset");
  $("dsSummary").textContent = `— ${stats.total} snippets · ${stats.languages.length} languages`;
  fillLangSelects(stats.languages);
  const max = Math.max(...Object.values(stats.per_language));
  $("langBars").innerHTML = Object.entries(stats.per_language).map(([lang, n]) => `
    <div class="lang-bar-row"><span>${lang}</span>
      <div class="bar-track"><div class="bar-fill" style="width:${(n / max * 100).toFixed(0)}%"></div></div>
      <span>${n}</span></div>`).join("");
  loadSample();
}
async function loadSample() {
  const lang = $("browseLang").value;
  try {
    const d = await api(`/api/samples/${encodeURIComponent(lang)}`);
    $("sampleView").textContent = d.sample || "// no samples yet";
  } catch (e) { $("sampleView").textContent = "// " + e.message; }
}
$("browseLang")?.addEventListener("change", loadSample);
$("anotherBtn").addEventListener("click", loadSample);

$("addBtn").addEventListener("click", async () => {
  const language = $("addLang").value;
  const code = $("addCode").value;
  const msg = $("addMsg");
  msg.className = "msg";
  if (code.trim().length < 3) { msg.textContent = "Paste some code first."; msg.classList.add("err"); return; }
  try {
    const r = await api("/api/dataset/add", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ language, code }),
    });
    msg.textContent = `✓ Added to ${language}. Dataset now ${r.stats.total} snippets — models retrained.`;
    $("addCode").value = "";
    evalCache = null;
  } catch (e) { msg.textContent = "✗ " + e.message; msg.classList.add("err"); }
});

$("uploadBtn").addEventListener("click", async () => {
  const file = $("csvFile").files[0];
  const msg = $("uploadMsg");
  msg.className = "msg";
  if (!file) { msg.textContent = "Choose a CSV file first."; msg.classList.add("err"); return; }
  const fd = new FormData();
  fd.append("file", file);
  try {
    const r = await api("/api/dataset/upload", { method: "POST", body: fd });
    msg.textContent = `✓ ${r.added} snippets added. Dataset now ${r.stats.total} — models retrained.`;
    evalCache = null;
  } catch (e) { msg.textContent = "✗ " + e.message; msg.classList.add("err"); }
});
