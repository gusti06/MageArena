package magearena;

import java.util.Scanner;

public class Game {
    private final Player player;
    private final Enemy enemy;
    private final Scanner scanner;

    public Game(Scanner scanner) {
        this.player = new Player("Mage");
        this.enemy = new Enemy("Arena Beast");
        this.scanner = scanner;
    }

    public void start() {
        System.out.println("=== MageArena ===");
        System.out.println("Kalahkan Arena Beast untuk menang.");

        while (player.isAlive() && enemy.isAlive()) {
            printStatus();
            playerTurn();
            if (!enemy.isAlive()) {
                break;
            }
            enemyTurn();
        }

        if (player.isAlive()) {
            System.out.println("Selamat! Kamu menang.");
        } else {
            System.out.println("Game over. Coba lagi.");
        }
    }

    private void printStatus() {
        System.out.printf("%s HP: %d | Mana: %d%n", player.getName(), player.getHealth(), player.getMana());
        System.out.printf("%s HP: %d%n", enemy.getName(), enemy.getHealth());
    }

    private void playerTurn() {
        System.out.println("Pilih aksi: [1] Attack [2] Fireball [3] Recover Mana");
        String choice = scanner.nextLine().trim();
        int dealt;

        switch (choice) {
            case "2":
                dealt = player.castSpell(enemy);
                if (dealt == 0) {
                    System.out.println("Mana tidak cukup, serangan dibatalkan.");
                } else {
                    System.out.printf("Fireball mengenai %s sebesar %d damage.%n", enemy.getName(), dealt);
                }
                break;
            case "3":
                player.recoverMana(5);
                System.out.println("Mana bertambah 5.");
                break;
            case "1":
            default:
                dealt = player.attack(enemy);
                System.out.printf("%s menyerang %s sebesar %d damage.%n", player.getName(), enemy.getName(), dealt);
                break;
        }
    }

    private void enemyTurn() {
        int dealt = enemy.attack(player);
        System.out.printf("%s menyerang balik sebesar %d damage.%n", enemy.getName(), dealt);
    }
}
