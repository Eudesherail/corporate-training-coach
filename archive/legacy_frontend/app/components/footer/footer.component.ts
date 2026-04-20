import {Component} from "@angular/core";
import {Router} from "@angular/router";

@Component({
    selector: "app-footer",
    templateUrl: "./footer.component.html",
    styleUrls: ["./footer.component.scss"]
})
export class FooterComponent {

    constructor(private router: Router) {
    }

    public toImpressum(): void {
        this.router.navigate(["/imprint"]).then();
    }

    public toDatenschutz(): void {
        this.router.navigate(["/dse"]).then();
    }

    public toQuellen(): void {
        this.router.navigate(["/quellen"]).then();
    }

    public toDatenschutzGPT(): void {
        this.router.navigate(["/dse-gpt"]).then();
    }
}
