import java.util.Date;

public class FoodItem {
    private String name;
    private int calorie;
    private int protein;
    private Date expiryDate;
    static int quantity;

    public FoodItem(String name, int calorie, int protein,Date expiryDate){
        this.name=name;
        this.calorie=calorie;
        this.protein=protein;
        this.expiryDate=expiryDate;
        quantity=0;
    }

    public void increaseQuantity(){
        quantity ++;
    }
    public void decreaseQuantity(){
        quantity --;
    }
}
