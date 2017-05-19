package realself.crawler;

import java.util.List;
import java.util.Set;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.regex.Pattern;

import org.apache.solr.client.solrj.SolrClient;
import org.apache.solr.client.solrj.impl.HttpSolrClient;
import org.apache.solr.common.SolrInputDocument;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import edu.uci.ics.crawler4j.crawler.Page;
import edu.uci.ics.crawler4j.crawler.WebCrawler;
import edu.uci.ics.crawler4j.parser.HtmlParseData;
import edu.uci.ics.crawler4j.url.WebURL;

public class RealselfCrawler extends WebCrawler {
    private int NO_OF_DOCUMENT_TO_COMMIT = 1;
    private List<SolrInputDocument> documentsIndexed = new CopyOnWriteArrayList<SolrInputDocument>();
    private final static Pattern FILTERS = Pattern.compile(".*(\\.(css|js|gif|jpg"
                                                           + "|png|mp3|mp3|zip|gz))$");

    //Q&A pages: https://www.realself.com/XXX/answers?page=YYY; X=field, Y=number
    //doctor pages: https://www.realself.com/find/XXX/YYY/ZZZ; X=country, Y=field, Z=doctor
    
    /**
     * This method receives two parameters. The first parameter is the page
     * in which we have discovered this new url and the second parameter is
     * the new url. You should implement this function to specify whether
     * the given url should be crawled or not (based on your crawling logic).
     * In this example, we are instructing the crawler to ignore urls that
     * have css, js, git, ... extensions and to only accept urls that start
     * with "http://www.ics.uci.edu/". In this case, we didn't need the
     * referringPage parameter to make the decision.
     */
     @Override
     public boolean shouldVisit(Page referringPage, WebURL url) {
         String href = url.getURL().toLowerCase();
         return !FILTERS.matcher(href).matches()
                && href.startsWith("https://www.realself.com/");
     }

     /**
      * This function is called when a page is fetched and ready
      * to be processed by your program.
      */
     @Override
     public void visit(Page page) {
         String url = page.getWebURL().getURL();
         System.out.println("URL: " + url);

         if (page.getParseData() instanceof HtmlParseData) {
             HtmlParseData htmlParseData = (HtmlParseData) page.getParseData();
             String text = htmlParseData.getText();
             String html = htmlParseData.getHtml();
             Set<WebURL> links = htmlParseData.getOutgoingUrls();

             // Parsing Tags out of Jsoup
             Document doc = Jsoup.parse(html);
             SolrInputDocument doSolrInputDocument = new SolrInputDocument();
             doSolrInputDocument.setField("id", page.hashCode());
             Elements linksList = doc.getElementsByTag("a");
             String serverUrl = "http://localhost:8983/solr/collection1";
             SolrClient solr = new HttpSolrClient.Builder(serverUrl).build();
                          
             // To do : replace the logic with async-io for faster execution.
             for (Element link : linksList) {
               String linkHref = link.attr("href");
               System.out.println(linkHref + "printed attribute \n");
               String linkText = link.text();
               System.out.println(linkText + "printed text \n");
               doSolrInputDocument.setField("features", linkHref);;
             }
             
             Elements paragraphList = doc.getElementsByTag("p");
             for (Element parElement : paragraphList) {
             	String paragraphText = parElement.text();
             	System.out.println(paragraphText + "printed para text \n");
             	doSolrInputDocument.setField("features", paragraphText);
             }
             
             documentsIndexed.add(doSolrInputDocument);
             
             /*
              * Reducing the number of commits. 
              * To do : Replace commit with auto-commit on server side.
              * http://stackoverflow.com/questions/17654266/solr-autocommit-vs-autosoftcommit
              * To do : Replace add with async-io (Akka) since adds are blocking the thread.
              */
             if(documentsIndexed.size() > NO_OF_DOCUMENT_TO_COMMIT) {
                 try {
                 	solr.add(doSolrInputDocument);
                 	
                 	solr.commit(true, true);
                 } catch(Exception e) {
                 	System.out.println(e.getMessage());
                 	e.printStackTrace();
                 }
             }
             System.out.println("Text length: " + text.length());
             System.out.println("Html length: " + html.length());
             System.out.println("Number of outgoing links: " + links.size());
         }
    }
}
