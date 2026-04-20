import {Component, OnInit, ViewChild} from "@angular/core";
import {NgbAlert} from "@ng-bootstrap/ng-bootstrap";
import {Alert, AlertService} from "../../_helper/alert.service";

@Component({
    selector: "app-alert",
    templateUrl: "./alert.component.html",
    styleUrls: ["./alert.component.scss"]
})
export class AlertComponent implements OnInit {

    @ViewChild("alert", {static: false})
    alert: NgbAlert = {} as NgbAlert;

    constructor(public alertService: AlertService) {
    }

    ngOnInit(): void {
        setTimeout(() => this.alert.close(), 8000);
    }

    public close(alert: Alert): void {
        this.alertService.alerts = this.alertService.alerts.filter(x => x !== alert);
    }
}
