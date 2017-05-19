package realself;

import java.io.IOException;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.scene.layout.AnchorPane;
import javafx.scene.layout.BorderPane;
import javafx.stage.Stage;
import realself.crawler.RealselfCrawlController;
import realself.view.RootViewController;
import realself.view.SearchViewController;

public class Main extends Application {
    private Stage primaryStage;
    private BorderPane rootLayout;
    
    private RealselfCrawlController crawlController;

    @Override
    public void start(Stage primaryStage) {
        this.primaryStage = primaryStage;
        this.primaryStage.setTitle("AddressApp");

        initRootLayout();

        showSearchView();
    }

    /**
     * Initializes the root layout.
     */
    public void initRootLayout() {
        try {
            // Load root layout from fxml file.
            FXMLLoader loader = new FXMLLoader();
            loader.setLocation(Main.class.getResource("view/RootView.fxml"));
            this.rootLayout = (BorderPane) loader.load();

            // Connect to the controller.
            RootViewController rvController = loader.getController();
            rvController.setMain(this);
            
            // Show the scene containing the root layout.
            Scene scene = new Scene(this.rootLayout);
            this.primaryStage.setScene(scene);
            this.primaryStage.show();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    
    /**
     * Shows the search view inside the root view.
     */
    public void showSearchView() {
        try {
            // Load person overview.
            FXMLLoader loader = new FXMLLoader();
            loader.setLocation(Main.class.getResource("./view/SearchView.fxml"));
            AnchorPane personOverview = (AnchorPane) loader.load();

            // Set search view into the center of root layout.
            this.rootLayout.setCenter(personOverview);

            // Give the controller access to the main app.
            SearchViewController svController = loader.getController();
            svController.setMain(this);

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * Returns the main stage.
     * @return
     */
    public Stage getPrimaryStage() {
        return this.primaryStage;
    }
    
    public RealselfCrawlController getCrawlController() {
    	if(this.crawlController == null) {
    		try{
    			this.crawlController = new RealselfCrawlController();
    		} catch(Exception e) {
    			//TODO Dialog
    		}
    	}
    	
    	return this.crawlController;
    }

    public static void main(String[] args) {
        launch(args);
    }
}