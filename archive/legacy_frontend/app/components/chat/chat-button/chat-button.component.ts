import {Component, EventEmitter, Input, Output} from "@angular/core";

@Component({
    selector: "app-chat-button",
    templateUrl: "./chat-button.component.html",
    styleUrls: ["./chat-button.component.scss"]
})
export class ChatButtonComponent {
    @Output() clicked = new EventEmitter();
    @Input() isOpen!: boolean;

// Define the toggleChatWindow method to toggle the state of the chat window and emit the 'clicked' event
    toggleChatWindow() {
        this.isOpen = !this.isOpen;
        this.clicked.emit();
    }
}
