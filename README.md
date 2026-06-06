# MageArena

Tugas Besar Matakuliah Pemrograman Berorientasi Object (membuat game).

Implementasi saat ini adalah game turn-based sederhana berbasis terminal untuk menunjukkan konsep OOP:
- Encapsulation (atribut private/protected + method publik)
- Inheritance (`Player` dan `Enemy` mewarisi `Character`)
- Polymorphism (override `attack`)
- Abstraction (`Character` sebagai abstract class)

## Cara Menjalankan

```bash
javac -d /tmp/magearena-out src/main/java/magearena/*.java
java -cp /tmp/magearena-out magearena.Main
```
