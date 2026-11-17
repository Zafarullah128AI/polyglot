"""Build Polyglot dataset: 10 languages x 20 original code snippets (200 rows).

Every snippet below was written for this project (original sample data).
Columns: language, code, lines, chars, length_bucket
  short  = 1-3 lines, medium = 4-10 lines, long = 11+ lines
"""
import csv
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.csv")

DATA = {}

DATA["Python"] = [
    r'''print("Hello, World!")''',
    r'''def greet(name):
    return f"Hello, {name}!"

print(greet("Tarique"))''',
    r'''def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        print(a, end=" ")
        a, b = b, a + b

fibonacci(10)''',
    r'''numbers = [1, 2, 3, 4, 5]
squares = [x * x for x in numbers]
print(squares)''',
    r'''class Student:
    def __init__(self, name, roll):
        self.name = name
        self.roll = roll

    def show(self):
        print(f"{self.name} - {self.roll}")

s = Student("Tarique", "24BSIT118")
s.show()''',
    r'''total = 0
for i in range(1, 101):
    total += i
print("Sum:", total)''',
    r'''marks = {"Ali": 85, "Sara": 92, "Bilal": 78}
for name, score in marks.items():
    if score >= 90:
        print(name, "passed with distinction")''',
    r'''try:
    with open("notes.txt") as f:
        text = f.read()
    print(len(text.split()), "words")
except FileNotFoundError:
    print("File not found")''',
    r'''nums = [5, 2, 9, 1, 7]
evens = list(filter(lambda x: x % 2 == 0, nums))
print(sorted(evens))''',
    r'''def main():
    print("Program started")

if __name__ == "__main__":
    main()''',
    r'''count = 0
while count < 5:
    print("Count:", count)
    count += 1''',
    r'''a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
print("Common:", a & b)
print("Union:", a | b)''',
    r'''names = ["Ali", "Sara", "Bilal"]
for i, name in enumerate(names, start=1):
    print(i, name)''',
    r'''text = "machine learning"
print(text[::-1].upper())''',
    r'''import json

data = {"name": "Tarique", "cgpa": 3.5}
text = json.dumps(data)
print(text)
loaded = json.loads(text)
print(loaded["cgpa"])''',
    r'''from datetime import datetime

now = datetime.now()
print(now.strftime("%d %B %Y, %I:%M %p"))''',
    r'''import random

choices = ["rock", "paper", "scissors"]
print("Computer picked:", random.choice(choices))''',
    r'''def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print(factorial(5))''',
    r'''def repeat(times):
    def decorator(func):
        def wrapper(*args):
            for _ in range(times):
                func(*args)
        return wrapper
    return decorator

@repeat(3)
def hello():
    print("Hi!")

hello()''',
    r'''students = [
    {"name": "Ali", "marks": 85},
    {"name": "Sara", "marks": 92},
    {"name": "Bilal", "marks": 78},
]
top = max(students, key=lambda s: s["marks"])
print(top["name"], "is the topper")''',
]

DATA["JavaScript"] = [
    r'''console.log("Hello, World!");''',
    r'''const greet = (name) => `Hello, ${name}!`;
console.log(greet("Tarique"));''',
    r'''const numbers = [1, 2, 3, 4, 5];
const doubled = numbers.map(n => n * 2);
console.log(doubled);''',
    r'''async function getUser(id) {
  const res = await fetch(`https://api.example.com/users/${id}`);
  const data = await res.json();
  return data;
}''',
    r'''class Student {
  constructor(name, roll) {
    this.name = name;
    this.roll = roll;
  }
  show() {
    console.log(`${this.name} - ${this.roll}`);
  }
}
const s = new Student("Tarique", "24BSIT118");
s.show();''',
    r'''const scores = [85, 92, 78, 95];
let total = 0;
for (const s of scores) {
  total += s;
}
console.log("Average:", total / scores.length);''',
    r'''const user = { name: "Tarique", age: 21, city: "Nawabshah" };
const { name, city } = user;
console.log(name, "lives in", city);''',
    r'''const price = 1200;
const msg = `Total bill: Rs ${price * 1.17} (with tax)`;
console.log(msg);''',
    r'''fetch("https://api.example.com/posts")
  .then(res => res.json())
  .then(posts => console.log(posts.length, "posts loaded"))
  .catch(err => console.error("Failed:", err));''',
    r'''const cart = [{ price: 500 }, { price: 300 }, { price: 250 }];
const total = cart.reduce((sum, item) => sum + item.price, 0);
console.log("Cart total:", total);''',
    r'''setTimeout(() => {
  console.log("This runs after 2 seconds");
}, 2000);''',
    r'''const raw = '{"name": "Ali", "marks": 88}';
const obj = JSON.parse(raw);
console.log(obj.marks);
console.log(JSON.stringify({ ok: true }));''',
    r'''const a = [1, 2, 3];
const b = [...a, 4, 5];
const merged = { ...{ x: 1 }, ...{ y: 2 } };
console.log(b, merged);''',
    r'''try {
  const n = Number("abc");
  if (isNaN(n)) throw new Error("Not a number");
} catch (e) {
  console.log("Error:", e.message);
}''',
    r'''["apple", "banana", "mango"].forEach((fruit, i) => {
  console.log(i + 1, fruit);
});''',
    r'''function power(base, exp = 2) {
  return base ** exp;
}
console.log(power(5));
console.log(power(2, 3));''',
    r'''const visits = new Map();
visits.set("home", 12);
visits.set("about", 4);
console.log("Home visits:", visits.get("home"));''',
    r'''document.addEventListener("click", (event) => {
  console.log("Clicked at", event.clientX, event.clientY);
});''',
    r'''const user = { profile: { name: "Sara" } };
const name = user.profile?.name ?? "Guest";
console.log(name);''',
    r'''export function add(a, b) {
  return a + b;
}
import { add } from "./math.js";
console.log(add(2, 3));''',
]

DATA["TypeScript"] = [
    r'''function add(a: number, b: number): number {
  return a + b;
}
console.log(add(4, 5));''',
    r'''interface User {
  id: number;
  name: string;
  email?: string;
}

const user: User = { id: 1, name: "Tarique" };''',
    r'''type Status = "active" | "pending" | "closed";
let order: Status = "pending";
console.log(order);''',
    r'''function first<T>(items: T[]): T | undefined {
  return items[0];
}
console.log(first<number>([10, 20, 30]));''',
    r'''enum Role {
  Admin = "ADMIN",
  Student = "STUDENT",
  Teacher = "TEACHER",
}
const myRole: Role = Role.Student;''',
    r'''class BankAccount {
  private balance: number = 0;

  constructor(public owner: string) {}

  deposit(amount: number): void {
    this.balance += amount;
  }
}''',
    r'''const marks: number[] = [80, 90, 75];
const passed: string[] = marks
  .filter(m => m >= 80)
  .map(m => `Score ${m}`);
console.log(passed);''',
    r'''interface Product {
  title: string;
  price: number;
  discount?: number;
}

function finalPrice(p: Product): number {
  return p.price - (p.discount ?? 0);
}''',
    r'''interface Animal {
  speak(): void;
}

class Dog implements Animal {
  speak(): void {
    console.log("Woof!");
  }
}''',
    r'''function describe(value: string | number): string {
  if (typeof value === "string") {
    return `Text: ${value}`;
  }
  return `Number: ${value}`;
}''',
    r'''class Config {
  readonly apiKey: string = "abc123";
  readonly timeout: number = 5000;
}''',
    r'''type Point = [number, number];
const origin: Point = [0, 0];
console.log(origin[0], origin[1]);''',
    r'''async function loadData(): Promise<string> {
  const res = await fetch("/api/data");
  return await res.text();
}''',
    r'''const user = { name: "Ali" } as { name: string; age?: number };
console.log(user.name);''',
    r'''const scores: Record<string, number> = {
  Ali: 85,
  Sara: 92,
};
console.log(scores["Sara"]);''',
    r'''function greet(name: string): void;
function greet(name: string, title: string): void;
function greet(name: string, title?: string): void {
  console.log(title ? `${title} ${name}` : name);
}''',
    r'''abstract class Shape {
  abstract area(): number;
}

class Circle extends Shape {
  constructor(private r: number) {
    super();
  }
  area(): number {
    return Math.PI * this.r * this.r;
  }
}''',
    r'''type Theme = "light" | "dark";
let theme: Theme = "dark";
console.log(theme);''',
    r'''interface Todo {
  id: number;
  text: string;
  done: boolean;
}

function updateTodo(todo: Todo, patch: Partial<Todo>): Todo {
  return { ...todo, ...patch };
}''',
    r'''interface Named {
  name: string;
}

interface Student extends Named {
  roll: string;
}

const s: Student = { name: "Tarique", roll: "24BSIT118" };''',
]

DATA["Java"] = [
    r'''public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}''',
    r'''import java.util.ArrayList;

public class Main {
    public static void main(String[] args) {
        ArrayList<String> names = new ArrayList<>();
        names.add("Ali");
        names.add("Sara");
        for (String n : names) {
            System.out.println(n);
        }
    }
}''',
    r'''public class Student {
    private String name;
    private String roll;

    public Student(String name, String roll) {
        this.name = name;
        this.roll = roll;
    }

    public String getName() {
        return name;
    }
}''',
    r'''import java.util.HashMap;

public class Marks {
    public static void main(String[] args) {
        HashMap<String, Integer> marks = new HashMap<>();
        marks.put("Ali", 85);
        marks.put("Sara", 92);
        System.out.println(marks.get("Sara"));
    }
}''',
    r'''import java.io.*;

public class ReadFile {
    public static void main(String[] args) {
        try {
            BufferedReader br = new BufferedReader(new FileReader("notes.txt"));
            System.out.println(br.readLine());
            br.close();
        } catch (IOException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}''',
    r'''interface Drawable {
    void draw();
}

class Circle implements Drawable {
    public void draw() {
        System.out.println("Drawing circle");
    }
}''',
    r'''public class Factorial {
    static long fact(int n) {
        if (n <= 1) return 1;
        return n * fact(n - 1);
    }

    public static void main(String[] args) {
        System.out.println(fact(5));
    }
}''',
    r'''public class Sum {
    public static void main(String[] args) {
        int[] nums = {3, 7, 2, 9, 4};
        int total = 0;
        for (int i = 0; i < nums.length; i++) {
            total += nums[i];
        }
        System.out.println("Total: " + total);
    }
}''',
    r'''public class Reverse {
    public static void main(String[] args) {
        StringBuilder sb = new StringBuilder("hello");
        System.out.println(sb.reverse().toString());
    }
}''',
    r'''import java.util.Scanner;

public class Input {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter your name: ");
        String name = sc.nextLine();
        System.out.println("Hello " + name);
        sc.close();
    }
}''',
    r'''enum Day {
    MONDAY, TUESDAY, WEDNESDAY
}

public class Today {
    public static void main(String[] args) {
        Day d = Day.MONDAY;
        System.out.println(d);
    }
}''',
    r'''class Animal {
    void sound() {
        System.out.println("Some sound");
    }
}

class Dog extends Animal {
    void sound() {
        System.out.println("Bark");
    }
}''',
    r'''import java.util.*;
import java.util.stream.*;

public class Streams {
    public static void main(String[] args) {
        List<Integer> nums = Arrays.asList(1, 2, 3, 4, 5);
        List<Integer> evens = nums.stream()
            .filter(n -> n % 2 == 0)
            .collect(Collectors.toList());
        System.out.println(evens);
    }
}''',
    r'''public class Worker implements Runnable {
    public void run() {
        System.out.println("Working in a thread");
    }

    public static void main(String[] args) {
        new Thread(new Worker()).start();
    }
}''',
    r'''public class Grade {
    public static void main(String[] args) {
        int marks = 85;
        String grade = switch (marks / 10) {
            case 9, 10 -> "A";
            case 8 -> "B";
            default -> "C";
        };
        System.out.println(grade);
    }
}''',
    r'''import java.util.List;

public class Generics {
    public static void printAll(List<String> items) {
        for (String item : items) {
            System.out.println(item);
        }
    }
}''',
    r'''import java.util.Random;

public class Dice {
    public static void main(String[] args) {
        Random rand = new Random();
        System.out.println("Rolled: " + (rand.nextInt(6) + 1));
    }
}''',
    r'''public class Format {
    public static void main(String[] args) {
        String msg = String.format("Name: %s, Marks: %d", "Ali", 88);
        System.out.println(msg);
    }
}''',
    r'''abstract class Shape {
    abstract double area();
}

class Square extends Shape {
    double side;
    Square(double side) {
        this.side = side;
    }
    double area() {
        return side * side;
    }
}''',
    r'''import java.util.List;

public class Modern {
    public static void main(String[] args) {
        var names = List.of("Ali", "Sara", "Bilal");
        names.forEach(n -> System.out.println(n));
    }
}''',
]

DATA["C"] = [
    r'''#include <stdio.h>

int main() {
    printf("Hello, World!\n");
    return 0;
}''',
    r'''#include <stdio.h>

int main() {
    int sum = 0;
    for (int i = 1; i <= 100; i++) {
        sum += i;
    }
    printf("Sum: %d\n", sum);
    return 0;
}''',
    r'''#include <stdio.h>

int add(int a, int b) {
    return a + b;
}

int main() {
    printf("%d\n", add(4, 5));
    return 0;
}''',
    r'''#include <stdio.h>
#include <string.h>

struct Student {
    char name[50];
    int roll;
};

int main() {
    struct Student s = {"Tarique", 118};
    printf("%s %d\n", s.name, s.roll);
    return 0;
}''',
    r'''#include <stdio.h>

void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

int main() {
    int x = 5, y = 9;
    swap(&x, &y);
    printf("%d %d\n", x, y);
    return 0;
}''',
    r'''#include <stdio.h>
#include <stdlib.h>

int main() {
    int *arr = malloc(5 * sizeof(int));
    for (int i = 0; i < 5; i++) {
        arr[i] = i * 10;
    }
    free(arr);
    return 0;
}''',
    r'''#include <stdio.h>

int main() {
    int nums[] = {4, 2, 9, 1, 7};
    int n = sizeof(nums) / sizeof(nums[0]);
    int max = nums[0];
    for (int i = 1; i < n; i++) {
        if (nums[i] > max) max = nums[i];
    }
    printf("Max: %d\n", max);
    return 0;
}''',
    r'''#include <stdio.h>

int main() {
    int marks = 72;
    if (marks >= 80) {
        printf("Grade A\n");
    } else if (marks >= 60) {
        printf("Grade B\n");
    } else {
        printf("Grade C\n");
    }
    return 0;
}''',
    r'''#include <stdio.h>

int main() {
    int i = 0;
    while (i < 5) {
        printf("%d\n", i);
        i++;
    }
    return 0;
}''',
    r'''#include <stdio.h>
#include <string.h>

int main() {
    char a[] = "hello";
    char b[] = "hello";
    if (strcmp(a, b) == 0) {
        printf("Equal, length %lu\n", strlen(a));
    }
    return 0;
}''',
    r'''#include <stdio.h>

int main() {
    FILE *fp = fopen("data.txt", "r");
    if (fp == NULL) {
        printf("Cannot open file\n");
        return 1;
    }
    char line[100];
    while (fgets(line, sizeof(line), fp)) {
        printf("%s", line);
    }
    fclose(fp);
    return 0;
}''',
    r'''#include <stdio.h>

int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

int main() {
    printf("%d\n", factorial(6));
    return 0;
}''',
    r'''#include <stdio.h>

enum Color { RED, GREEN, BLUE };

int main() {
    enum Color c = GREEN;
    switch (c) {
        case RED:   printf("Red\n"); break;
        case GREEN: printf("Green\n"); break;
        default:    printf("Blue\n"); break;
    }
    return 0;
}''',
    r'''#include <stdio.h>

#define PI 3.14159
#define SQUARE(x) ((x) * (x))

int main() {
    printf("Area: %f\n", PI * SQUARE(5));
    return 0;
}''',
    r'''#include <stdio.h>

int main() {
    int table[3][3] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
    for (int r = 0; r < 3; r++) {
        for (int c = 0; c < 3; c++) {
            printf("%d ", table[r][c]);
        }
        printf("\n");
    }
    return 0;
}''',
    r'''#include <stdio.h>

int main() {
    int age;
    printf("Enter age: ");
    scanf("%d", &age);
    printf("You are %d years old\n", age);
    return 0;
}''',
    r'''#include <stdio.h>

void bubbleSort(int arr[], int n) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                int t = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = t;
            }
        }
    }
}''',
    r'''#include <stdio.h>

int main() {
    int arr[] = {10, 20, 30, 40};
    int *p = arr;
    printf("%d\n", *(p + 2));
    return 0;
}''',
    r'''#include <stdio.h>

int main() {
    int n;
    do {
        printf("Enter a positive number: ");
        scanf("%d", &n);
    } while (n <= 0);
    printf("Got %d\n", n);
    return 0;
}''',
    r'''#include <stdio.h>
#include <stdlib.h>

int cmp(const void *a, const void *b) {
    return (*(int *)a - *(int *)b);
}

int main() {
    int arr[] = {5, 2, 9, 1};
    qsort(arr, 4, sizeof(int), cmp);
    return 0;
}''',
]

DATA["C++"] = [
    r'''#include <iostream>

int main() {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}''',
    r'''#include <iostream>
#include <vector>

int main() {
    std::vector<int> nums = {1, 2, 3, 4, 5};
    int sum = 0;
    for (int n : nums) {
        sum += n;
    }
    std::cout << sum << std::endl;
    return 0;
}''',
    r'''#include <iostream>
#include <string>

class Student {
private:
    std::string name;
    int roll;
public:
    Student(std::string n, int r) : name(n), roll(r) {}
    void show() {
        std::cout << name << " - " << roll << std::endl;
    }
};''',
    r'''#include <iostream>
#include <map>

int main() {
    std::map<std::string, int> marks;
    marks["Ali"] = 85;
    marks["Sara"] = 92;
    std::cout << marks["Sara"] << std::endl;
    return 0;
}''',
    r'''#include <iostream>

template <typename T>
T maximum(T a, T b) {
    return (a > b) ? a : b;
}

int main() {
    std::cout << maximum<int>(4, 9) << std::endl;
    return 0;
}''',
    r'''#include <iostream>
#include <string>

int main() {
    std::string text = "machine learning";
    auto pos = text.find("learn");
    std::cout << "Found at " << pos << std::endl;
    return 0;
}''',
    r'''#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> v = {5, 2, 9, 1, 7};
    std::sort(v.begin(), v.end(), [](int a, int b) {
        return a < b;
    });
    for (int n : v) std::cout << n << " ";
    return 0;
}''',
    r'''#include <iostream>
#include <memory>

int main() {
    auto ptr = std::make_unique<int>(42);
    std::cout << *ptr << std::endl;
    return 0;
}''',
    r'''#include <iostream>

struct Point {
    int x;
    int y;
};

int main() {
    Point p{3, 4};
    std::cout << p.x << ", " << p.y << std::endl;
    return 0;
}''',
    r'''#include <iostream>
#include <stdexcept>

int main() {
    try {
        int x = 10, y = 0;
        if (y == 0) throw std::runtime_error("divide by zero");
        std::cout << x / y << std::endl;
    } catch (const std::exception& e) {
        std::cout << "Error: " << e.what() << std::endl;
    }
    return 0;
}''',
    r'''#include <iostream>
#include <set>

int main() {
    std::set<int> s = {3, 1, 4, 1, 5};
    for (int n : s) {
        std::cout << n << " ";
    }
    return 0;
}''',
    r'''#include <iostream>

int add(int a, int b) { return a + b; }
double add(double a, double b) { return a + b; }

int main() {
    std::cout << add(2, 3) << " " << add(2.5, 3.1) << std::endl;
    return 0;
}''',
    r'''#include <iostream>

class Animal {
public:
    virtual void sound() {
        std::cout << "Some sound" << std::endl;
    }
};

class Dog : public Animal {
public:
    void sound() override {
        std::cout << "Bark" << std::endl;
    }
};''',
    r'''#include <iostream>

int main() {
    int age;
    std::cout << "Enter age: ";
    std::cin >> age;
    std::cout << "Age is " << age << std::endl;
    return 0;
}''',
    r'''#include <iostream>
#include <vector>

int main() {
    std::vector<std::string> fruits = {"apple", "banana", "mango"};
    for (const auto& f : fruits) {
        std::cout << f << std::endl;
    }
    return 0;
}''',
    r'''#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> v = {3, 1, 4, 1, 5, 9};
    auto it = std::find_if(v.begin(), v.end(), [](int n) {
        return n > 5;
    });
    if (it != v.end()) std::cout << "Found " << *it << std::endl;
    return 0;
}''',
    r'''#include <iostream>

namespace math {
    int square(int x) { return x * x; }
}

int main() {
    std::cout << math::square(6) << std::endl;
    return 0;
}''',
    r'''#include <iostream>

class Complex {
public:
    double re, im;
    Complex(double r, double i) : re(r), im(i) {}
    Complex operator+(const Complex& o) {
        return Complex(re + o.re, im + o.im);
    }
};''',
    r'''#include <iostream>
#include <vector>
#include <algorithm>

bool longer(const std::string& a, const std::string& b) {
    return a.size() > b.size();
}

int main() {
    std::vector<std::string> words = {"cat", "elephant", "dog"};
    std::sort(words.begin(), words.end(), longer);
    std::cout << words[0] << std::endl;
    return 0;
}''',
    r'''#include <iostream>

enum class TrafficLight { Red, Yellow, Green };

int main() {
    TrafficLight light = TrafficLight::Green;
    if (light == TrafficLight::Green) {
        std::cout << "Go!" << std::endl;
    }
    return 0;
}''',
]

DATA["C#"] = [
    r'''using System;

class Program {
    static void Main() {
        Console.WriteLine("Hello, World!");
    }
}''',
    r'''using System;
using System.Collections.Generic;

class Program {
    static void Main() {
        var names = new List<string> { "Ali", "Sara", "Bilal" };
        foreach (var n in names) {
            Console.WriteLine(n);
        }
    }
}''',
    r'''public class Student {
    public string Name { get; set; }
    public string Roll { get; set; }

    public Student(string name, string roll) {
        Name = name;
        Roll = roll;
    }
}''',
    r'''using System;
using System.Collections.Generic;

class Program {
    static void Main() {
        var marks = new Dictionary<string, int>();
        marks["Ali"] = 85;
        marks["Sara"] = 92;
        Console.WriteLine(marks["Sara"]);
    }
}''',
    r'''using System;
using System.Linq;

class Program {
    static void Main() {
        int[] nums = { 1, 2, 3, 4, 5, 6 };
        var evens = nums.Where(n => n % 2 == 0)
                        .Select(n => n * 10);
        foreach (var n in evens) Console.WriteLine(n);
    }
}''',
    r'''using System;

class Program {
    static void Main() {
        try {
            int x = int.Parse("abc");
        } catch (FormatException ex) {
            Console.WriteLine("Bad input: " + ex.Message);
        }
    }
}''',
    r'''using System;

class Program {
    static void Main() {
        string name = "Tarique";
        int marks = 88;
        Console.WriteLine($"Student {name} scored {marks}%");
    }
}''',
    r'''using System;
using System.Threading.Tasks;

class Program {
    static async Task<string> FetchData() {
        await Task.Delay(500);
        return "data loaded";
    }

    static async Task Main() {
        Console.WriteLine(await FetchData());
    }
}''',
    r'''public interface IShape {
    double Area();
}

public class Square : IShape {
    public double Side { get; set; }
    public double Area() => Side * Side;
}''',
    r'''using System;

class Program {
    static void Main() {
        for (var i = 1; i <= 5; i++) {
            Console.WriteLine($"Count {i}");
        }
    }
}''',
    r'''using System;

class Program {
    static void Main() {
        int marks = 85;
        string grade = marks switch {
            >= 90 => "A",
            >= 80 => "B",
            _ => "C"
        };
        Console.WriteLine(grade);
    }
}''',
    r'''public enum Day {
    Monday,
    Tuesday,
    Wednesday
}

public class Today {
    public Day Current { get; set; } = Day.Monday;
}''',
    r'''public class Animal {
    public virtual void Sound() {
        Console.WriteLine("Some sound");
    }
}

public class Dog : Animal {
    public override void Sound() {
        Console.WriteLine("Bark");
    }
}''',
    r'''using System;
using System.IO;

class Program {
    static void Main() {
        string text = File.ReadAllText("notes.txt");
        Console.WriteLine(text.Length + " characters");
    }
}''',
    r'''using System;

class Program {
    static void Main() {
        string input = "42";
        int value = int.Parse(input);
        double price = Convert.ToDouble("19.99");
        Console.WriteLine(value + price);
    }
}''',
    r'''using System;
using System.Text;

class Program {
    static void Main() {
        var sb = new StringBuilder();
        sb.Append("Hello");
        sb.Append(" World");
        Console.WriteLine(sb.ToString());
    }
}''',
    r'''public record Person(string Name, int Age);

public class Demo {
    public void Show() {
        var p = new Person("Tarique", 21);
        System.Console.WriteLine(p.Name);
    }
}''',
    r'''using System;

class Program {
    static void Main() {
        int? age = null;
        int realAge = age ?? 0;
        Console.WriteLine("Age: " + realAge);
    }
}''',
    r'''using System;

class Program {
    static int Sum(params int[] numbers) {
        int total = 0;
        foreach (int n in numbers) total += n;
        return total;
    }

    static void Main() {
        Console.WriteLine(Sum(1, 2, 3, 4));
    }
}''',
    r'''using System;

class Program {
    static void Main() {
        Console.Write("Enter your name: ");
        string name = Console.ReadLine();
        Console.WriteLine("Hello " + name);
    }
}''',
]

DATA["Go"] = [
    r'''package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
}''',
    r'''package main

import "fmt"

func add(a, b int) int {
    return a + b
}

func main() {
    fmt.Println(add(4, 5))
}''',
    r'''package main

import "fmt"

func main() {
    nums := []int{1, 2, 3, 4, 5}
    total := 0
    for _, n := range nums {
        total += n
    }
    fmt.Println("Total:", total)
}''',
    r'''package main

import "fmt"

func main() {
    marks := map[string]int{
        "Ali":  85,
        "Sara": 92,
    }
    fmt.Println(marks["Sara"])
}''',
    r'''package main

import "fmt"

type Student struct {
    Name string
    Roll string
}

func (s Student) Show() {
    fmt.Println(s.Name, "-", s.Roll)
}

func main() {
    s := Student{"Tarique", "24BSIT118"}
    s.Show()
}''',
    r'''package main

import (
    "fmt"
    "time"
)

func worker(done chan bool) {
    time.Sleep(time.Second)
    done <- true
}

func main() {
    done := make(chan bool)
    go worker(done)
    <-done
    fmt.Println("Done")
}''',
    r'''package main

import (
    "fmt"
    "os"
)

func readFile(name string) error {
    _, err := os.ReadFile(name)
    if err != nil {
        return err
    }
    return nil
}

func main() {
    if err := readFile("notes.txt"); err != nil {
        fmt.Println("Error:", err)
    }
}''',
    r'''package main

import "fmt"

func main() {
    for i := 0; i < 5; i++ {
        fmt.Println("Count:", i)
    }
}''',
    r'''package main

import "fmt"

func main() {
    defer fmt.Println("This runs last")
    fmt.Println("This runs first")
}''',
    r'''package main

import "fmt"

func grade(marks int) string {
    switch {
    case marks >= 90:
        return "A"
    case marks >= 80:
        return "B"
    default:
        return "C"
    }
}

func main() {
    fmt.Println(grade(85))
}''',
    r'''package main

import "fmt"

func main() {
    arr := [3]string{"apple", "banana", "mango"}
    fmt.Println(len(arr), arr[0])
}''',
    r'''package main

import (
    "fmt"
    "strings"
)

func main() {
    text := "hello world"
    fmt.Println(strings.Contains(text, "world"))
    fmt.Println(strings.Split(text, " "))
}''',
    r'''package main

import "fmt"

type Speaker interface {
    Speak()
}

type Dog struct{}

func (d Dog) Speak() {
    fmt.Println("Bark")
}''',
    r'''package main

import "fmt"

func main() {
    nums := make([]int, 0, 5)
    nums = append(nums, 10, 20, 30)
    fmt.Println(nums)
}''',
    r'''package main

import "fmt"

func main() {
    name := "Tarique"
    marks := 88
    fmt.Printf("Student %s scored %d%%\n", name, marks)
}''',
    r'''package main

import (
    "fmt"
    "os"
)

func main() {
    args := os.Args
    fmt.Println("Program:", args[0])
    fmt.Println("Args:", args[1:])
}''',
    r'''package main

import "fmt"

func divide(a, b int) (int, error) {
    if b == 0 {
        return 0, fmt.Errorf("cannot divide by zero")
    }
    return a / b, nil
}''',
    r'''package main

import "fmt"

func main() {
    x := 10
    p := &x
    *p = 20
    fmt.Println(x)
}''',
    r'''package main

import (
    "fmt"
    "time"
)

func main() {
    now := time.Now()
    fmt.Println(now.Format("02 January 2006, 03:04 PM"))
}''',
    r'''package main

import (
    "encoding/json"
    "fmt"
)

type User struct {
    Name  string `json:"name"`
    Marks int    `json:"marks"`
}

func main() {
    data, _ := json.Marshal(User{"Ali", 88})
    fmt.Println(string(data))
}''',
]

DATA["Rust"] = [
    r'''fn main() {
    println!("Hello, World!");
}''',
    r'''fn add(a: i32, b: i32) -> i32 {
    a + b
}

fn main() {
    println!("{}", add(4, 5));
}''',
    r'''fn main() {
    let mut total = 0;
    for i in 1..=100 {
        total += i;
    }
    println!("Sum: {}", total);
}''',
    r'''fn main() {
    let nums = vec![1, 2, 3, 4, 5];
    let doubled: Vec<i32> = nums.iter().map(|x| x * 2).collect();
    println!("{:?}", doubled);
}''',
    r'''fn main() {
    let marks = 85;
    let grade = match marks {
        90..=100 => "A",
        80..=89 => "B",
        _ => "C",
    };
    println!("{}", grade);
}''',
    r'''struct Student {
    name: String,
    roll: String,
}

impl Student {
    fn show(&self) {
        println!("{} - {}", self.name, self.roll);
    }
}

fn main() {
    let s = Student { name: "Tarique".to_string(), roll: "24BSIT118".to_string() };
    s.show();
}''',
    r'''fn main() {
    let maybe: Option<i32> = Some(42);
    match maybe {
        Some(v) => println!("Got {}", v),
        None => println!("Nothing here"),
    }
}''',
    r'''fn main() {
    let mut text = String::from("Hello");
    text.push_str(", World!");
    println!("{}", text);
}''',
    r'''fn main() {
    for i in 0..5 {
        println!("Count: {}", i);
    }
}''',
    r'''fn main() {
    let value = Some(10);
    if let Some(v) = value {
        println!("Value is {}", v);
    }
}''',
    r'''fn divide(a: f64, b: f64) -> Result<f64, String> {
    if b == 0.0 {
        return Err("cannot divide by zero".to_string());
    }
    Ok(a / b)
}

fn main() {
    match divide(10.0, 2.0) {
        Ok(v) => println!("{}", v),
        Err(e) => println!("Error: {}", e),
    }
}''',
    r'''trait Speak {
    fn speak(&self);
}

struct Dog;

impl Speak for Dog {
    fn speak(&self) {
        println!("Bark");
    }
}''',
    r'''use std::collections::HashMap;

fn main() {
    let mut marks = HashMap::new();
    marks.insert("Ali", 85);
    marks.insert("Sara", 92);
    println!("{}", marks["Sara"]);
}''',
    r'''fn main() {
    let square = |x: i32| x * x;
    println!("{}", square(7));
}''',
    r'''fn print_len(s: &String) {
    println!("Length: {}", s.len());
}

fn main() {
    let text = String::from("hello");
    print_len(&text);
    println!("{}", text);
}''',
    r'''fn main() {
    let mut count = 0;
    let result = loop {
        count += 1;
        if count == 5 {
            break count * 2;
        }
    };
    println!("{}", result);
}''',
    r'''fn main() {
    let point = (3, 4);
    let (x, y) = point;
    println!("{} {}", x, y);
}''',
    r'''const MAX_SCORE: i32 = 100;
static SCHOOL: &str = "SBBU";

fn main() {
    println!("{} - {}", SCHOOL, MAX_SCORE);
}''',
    r'''fn main() {
    let name = "Tarique";
    let marks = 88;
    println!("Student {} scored {}%", name, marks);
}''',
    r'''use std::io;

fn main() {
    println!("Enter your name:");
    let mut input = String::new();
    io::stdin().read_line(&mut input).unwrap();
    println!("Hello {}", input.trim());
}''',
]

DATA["PHP"] = [
    r'''<?php
echo "Hello, World!";
?>''',
    r'''<?php
function greet($name) {
    return "Hello, $name!";
}
echo greet("Tarique");
?>''',
    r'''<?php
$nums = [1, 2, 3, 4, 5];
foreach ($nums as $n) {
    echo $n * 2 . " ";
}
?>''',
    r'''<?php
$user = [
    "name" => "Tarique",
    "roll" => "24BSIT118",
    "cgpa" => 3.5
];
echo $user["name"] . " - " . $user["cgpa"];
?>''',
    r'''<?php
class Student {
    public $name;
    private $roll;

    public function __construct($name, $roll) {
        $this->name = $name;
        $this->roll = $roll;
    }

    public function show() {
        echo $this->name . " - " . $this->roll;
    }
}
?>''',
    r'''<?php
$marks = 72;
if ($marks >= 80) {
    echo "Grade A";
} elseif ($marks >= 60) {
    echo "Grade B";
} else {
    echo "Grade C";
}
?>''',
    r'''<?php
for ($i = 1; $i <= 10; $i++) {
    echo $i . " ";
}
?>''',
    r'''<?php
$name = $_GET["name"] ?? "Guest";
echo "Welcome, " . htmlspecialchars($name);
?>''',
    r'''<?php
$text = "machine learning";
echo strlen($text) . "\n";
echo strtoupper($text) . "\n";
echo str_replace("machine", "deep", $text);
?>''',
    r'''<?php
$nums = [5, 2, 9, 1, 7];
$evens = array_filter($nums, fn($n) => $n % 2 == 0);
$doubled = array_map(fn($n) => $n * 2, $evens);
print_r($doubled);
?>''',
    r'''<?php
try {
    $file = file_get_contents("missing.txt");
    if ($file === false) {
        throw new Exception("File not found");
    }
} catch (Exception $e) {
    echo "Error: " . $e->getMessage();
}
?>''',
    r'''<?php
$data = ["name" => "Ali", "marks" => 88];
$json = json_encode($data);
echo $json . "\n";
$back = json_decode($json, true);
echo $back["marks"];
?>''',
    r'''<?php
include "header.php";
echo "Page content here";
require "footer.php";
?>''',
    r'''<?php
$day = "Monday";
switch ($day) {
    case "Monday":
        echo "Start of week";
        break;
    case "Friday":
        echo "Jummah Mubarak";
        break;
    default:
        echo "Midweek";
}
?>''',
    r'''<?php
$i = 0;
while ($i < 5) {
    echo "Count: $i\n";
    $i++;
}
?>''',
    r'''<?php
$fruits = ["apple", "banana", "mango"];
echo implode(", ", $fruits) . "\n";
$parts = explode(" ", "hello world today");
print_r($parts);
?>''',
    r'''<?php
$email = $_POST["email"] ?? "";
if (isset($email) && !empty($email)) {
    echo "Email set: $email";
} else {
    echo "No email given";
}
?>''',
    r'''<?php
echo date("d F Y, h:i A") . "\n";
echo date("Y-m-d", strtotime("+7 days"));
?>''',
    r'''<?php
class Counter {
    public static $count = 0;

    public static function hit() {
        self::$count++;
        return self::$count;
    }
}
echo Counter::hit();
?>''',
    r'''<?php
$name = "Tarique";
$text = <<<EOT
Hello $name,
Welcome to the ML exhibition.
Good luck!
EOT;
echo $text;
?>''',
]


def bucket(lines: int) -> str:
    if lines <= 3:
        return "short"
    if lines <= 10:
        return "medium"
    return "long"


def main():
    rows = []
    for lang, snippets in DATA.items():
        for code in snippets:
            code = code.strip("\n")
            lines = code.count("\n") + 1
            rows.append({
                "language": lang,
                "code": code,
                "lines": lines,
                "chars": len(code),
                "length_bucket": bucket(lines),
            })
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["language", "code", "lines", "chars", "length_bucket"])
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {len(rows)} rows to {OUT}")
    from collections import Counter
    print("Per language:", dict(Counter(r["language"] for r in rows)))
    print("Per bucket:", dict(Counter(r["length_bucket"] for r in rows)))
    for lang in DATA:
        print(f"  {lang}: {len(DATA[lang])} snippets")


if __name__ == "__main__":
    main()
