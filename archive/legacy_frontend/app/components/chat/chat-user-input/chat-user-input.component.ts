import {Overlay, OverlayRef} from "@angular/cdk/overlay";
import {ComponentPortal} from "@angular/cdk/portal";
import {Component, ElementRef, EventEmitter, Input, Output, ViewChild} from "@angular/core";
import {ChatService} from "../../../api/chat/chat.service";
import {EmojiFensterComponent} from "./emoji-fenster/emoji-fenster.component";

@Component({
    selector: "app-chat-user-input",
    templateUrl: "./chat-user-input.component.html",
    styleUrls: ["./chat-user-input.component.scss"]
})
export class ChatUserInputComponent {
    userInput: string = "";
    private overlayRef!: OverlayRef;
    
    @ViewChild("focusMe") focusMe!: ElementRef<HTMLInputElement>;

    // Output property to send back the user input
    @Output() sendUserInput = new EventEmitter<string>();

    constructor(private overlay: Overlay, private chatBotService: ChatService, private elementRef: ElementRef) {
    }

    // Function to send back and reset the userInput
    @Input() set isOpen(isOpen: boolean) {
        if (isOpen) this.focusMe.nativeElement.focus();
    }
    
    onSubmit() {
        if (this.userInput && this.userInput.trim().length !== 0) {
            this.sendUserInput.emit(String(this.userInput.trim()));
            this.userInput = "";
        }
    }

    openOverlay(): void {
        this.chatBotService.makeEmojiVisible();
        const targetElement = this.elementRef.nativeElement.querySelector("#overlayTarget");


        if (this.overlayRef && this.overlayRef.hasAttached()) {
            this.overlayRef.detach(); // Overlay schließen, wenn bereits angezeigt
            return;
        }

        this.overlayRef = this.overlay.create({
            positionStrategy: this.overlay.position().flexibleConnectedTo(targetElement).withPositions([
                {originX: "end", originY: "bottom", overlayX: "start", overlayY: "top"}
            ]),
            scrollStrategy: this.overlay.scrollStrategies.block(),
            width: "0",
            height: "0",
        });

        const portal = new ComponentPortal(EmojiFensterComponent);
        const componentRef = this.overlayRef.attach(portal);

        componentRef.instance.closeEmoji.subscribe(() => {
            this.closeOverlay();
        });
        //Display beim Click außerhalb des Overlays schließen
        this.overlayRef.detachBackdrop(); //detach backdrop to make clickable out of the overlay
        //Event Listener Observable to dispose itself:
        this.overlayRef.outsidePointerEvents().subscribe(() => {
            this.chatBotService.makeEmojiVisible();
            this.overlayRef.dispose();
        });


        this.handleEmojiAddition();
    }

    closeOverlay() {
        this.openOverlay();
    }

    async handleEmojiAddition() {
        while (this.chatBotService.isEmojiPickerVisible) {
            if (this.chatBotService.EmojiAdd) {
                this.userInput = `${this.userInput}${this.userInputEmoj}`;
                this.chatBotService.EmojiAdd = false;
            }
            await this.delay(100); // Warte 100 Millisekunden, bevor du erneut überprüfst
        }
    }

    get userInputEmoj(): string {
        return this.chatBotService.userInput;
    }

    delay(ms: number) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    
    // Textarea passt die Höhe des Textes an, wenn es mehr als eine Zeile ist
    public adjustLineHeight($event: Event): void {
        const textArea = $event.target as HTMLTextAreaElement;
        if (textArea.scrollHeight > (textArea.offsetHeight*2)) {
            textArea.style.height = textArea.offsetHeight + "px";
            textArea.style.lineHeight = "normal";
            textArea.style.overflow = "auto";
        }
    }
}
