import {Component, EventEmitter, Input, OnInit, Output} from "@angular/core";
import {SafeResourceUrl } from '@angular/platform-browser'

@Component({
    selector: "app-chat-message",
    templateUrl: "./chat-message.component.html",
    styleUrls: ["./chat-message.component.scss"]
})
export class ChatMessageComponent implements OnInit {
    @Input() messageText!: string;
    @Input() messageTime!: string;
    @Input() messageHasVideo!: boolean;
    @Input() messageVideo!: string | SafeResourceUrl;
    @Input() messageImage!: string;
    @Input() isUser!: boolean;
    @Input() messageButtons!: { title: string; payload: string }[];
    @Input() isTyping: boolean = false;

    @Output() buttonClick: EventEmitter<{ title: string; payload: string }> = new EventEmitter<{
        title: string;
        payload: string
    }>();

    ngOnInit() {
    }

    // Method for buttons in the chatbot. Emit the 'buttonClick' event with the provided payload.
    onButtonClick(button: { title: string; payload: string }): void {
        this.buttonClick.emit(button);
    }
}
