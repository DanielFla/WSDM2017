package realself.view;

import javafx.fxml.FXML;
import javafx.scene.control.Label;
import javafx.scene.control.TableColumn;
import javafx.scene.control.MenuItem;
import realself.Main;

public class RootViewController {
    @FXML
    private MenuItem menuButtonCrawlNow;
   

    // Reference to the main application.
    private Main main;

    /**
     * The constructor.
     * The constructor is called before the initialize() method.
     */
    public RootViewController() {
    }

    /**
     * Initializes the controller class. This method is automatically called
     * after the fxml file has been loaded.
     */
    @FXML
    private void initialize() {
        // Initialize the person table with the two columns.
        //firstNameColumn.setCellValueFactory(cellData -> cellData.getValue().firstNameProperty());
    }

    /**
     * Is called by the main application to give a reference back to itself.
     * 
     * @param mainApp
     */
    public void setMain(Main main) {
        this.main = main;

        // Add observable list data to the table
        //personTable.setItems(main.getPersonData());
    }
    
    /**
     * Called when the user clicks on the Now button in the Crawl Menu.
     */
    @FXML
    private void handleCrawlNow() {
    	this.main.getCrawlController().startCrawl();
    }


}