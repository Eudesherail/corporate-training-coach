import { Component } from '@angular/core';

@Component({
  selector: 'app-bdsg',
  templateUrl: './bdsg.component.html',
  styleUrls: ['./bdsg.component.scss']
})
export class BdsgComponent {
    // Nutzung eines Kontaktformulars
    featureKontaktformular = false;
    
    // Nutzung von Cookies
    featureCookies = false;
    
    // Nutzung eines Newsletters
    featureNewsletter = false;
    
    // Nutzung von Google AdWords
    featureGoogleAdWords = false;
    
    // Nutzung von Google Analytics
    featureGoogleAnalytics = false;
    
    // Nutzung von Google Analytics Remarketing
    featureGoogleAnalyticsRemarketing = false;
    
    // Nutzung von Google Maps
    featureGoogleMaps = false;
    
    // Nutzung von Google Web Fonts
    featureGoogleWebFonts = false;
    
    // Datenschutzerklärung für die Nutzung von YouTube
    featureYouTube = true;
}
