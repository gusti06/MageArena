package magearena;

public class Player extends Character {
    private static final int MAX_MANA = 30;
    private int mana;

    public Player(String name) {
        super(name, 100, 12);
        this.mana = MAX_MANA;
    }

    public int getMana() {
        return mana;
    }

    public int castSpell(Character target) {
        final int manaCost = 10;
        final int spellDamage = 25;

        if (mana < manaCost) {
            return 0;
        }
        mana -= manaCost;
        return target.takeDamage(spellDamage);
    }

    public void recoverMana(int amount) {
        if (amount > 0) {
            mana = Math.min(MAX_MANA, mana + amount);
        }
    }
}
