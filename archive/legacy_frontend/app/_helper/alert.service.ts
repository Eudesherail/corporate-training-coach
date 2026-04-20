import {Injectable} from "@angular/core";

@Injectable({
  providedIn: "root"
})
export class AlertService {
  alerts: Alert[] = [];

  constructor() {
  }

  public error(message: string): void {
    this.addAlert("danger", message);
  }

  public warn(message: string): void {
    this.addAlert("warning", message);
  }

  public info(message: string): void {
    this.addAlert("info", message);
  }

  private addAlert(type: AlertType, message: string): void {
    if (!this.alerts.find(alert => alert.message === message)) {
      this.alerts.push(new Alert(type, message));
    }
  }
}

export class Alert {
  type: AlertType;
  message: string;

  constructor(type: AlertType, message: string) {
    this.type = type;
    this.message = message;
  }
}

type AlertType = "success" | "info" | "warning" | "danger" | "primary" | "secondary" | "light" | "dark";
