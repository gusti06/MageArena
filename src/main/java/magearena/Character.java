package magearena;

public abstract class Character {
    private final String name;
    private int health;
    private final int attackPower;

    protected Character(String name, int health, int attackPower) {
        if (health <= 0) {
            throw new IllegalArgumentException("Health must be greater than zero.");
        }
        if (attackPower <= 0) {
            throw new IllegalArgumentException("Attack power must be greater than zero.");
        }
        this.name = name;
        this.health = health;
        this.attackPower = attackPower;
    }

    public String getName() {
        return name;
    }

    public int getHealth() {
        return health;
    }

    public int getAttackPower() {
        return attackPower;
    }

    public boolean isAlive() {
        return health > 0;
    }

    public int attack(Character target) {
        return target.takeDamage(attackPower);
    }

    public int takeDamage(int damage) {
        if (damage <= 0) {
            return 0;
        }
        int actualDamage = Math.min(damage, health);
        health -= actualDamage;
        return actualDamage;
    }
}
