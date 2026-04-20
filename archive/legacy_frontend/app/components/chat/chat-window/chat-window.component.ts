import {AfterViewChecked, ChangeDetectorRef, Component, ElementRef, OnInit} from "@angular/core";
import {DomSanitizer, SafeResourceUrl} from "@angular/platform-browser"
import {ChatService} from "../../../api/chat/chat.service";
import {Message} from "../../../api/chat/message.model";
import {GoalService} from "../../../api/goal/goal.service";

@Component({
    selector: "app-chat-window",
    templateUrl: "./chat-window.component.html",
    styleUrls: ["./chat-window.component.scss"]
})
export class ChatWindowComponent implements OnInit, AfterViewChecked {
    isOpen = true;
    isFullScreen = false;
    messages: Message[] = [];
    isTyping: boolean = false;
    firstMessage: Message = {
        text: "Hi",
        hasVideo: false,
        video: "",
        image: "",
        time: "14:34",
        isUser: false,
        buttons: ""
    }
    embededLink!: string | SafeResourceUrl;
    messageHasVideo = false;

    constructor(private chatbotService: ChatService,
                private el: ElementRef,
                private cdr: ChangeDetectorRef,
                private goalService: GoalService,
                private sanitizer: DomSanitizer) {
    }

    async ngOnInit() {
        this.isOpen = false;
        this.isFullScreen = false;
        this.createFirstMessage();
        // const text = await this.createFirstMessage();
        // console.log(text)
        // this.firstMessage.text = await this.createFirstMessage();
        // console.log(this.firstMessage)
        // this.addBotMessage(this.firstMessage)

    }

    ngAfterViewChecked(): void {
        this.cdr.detectChanges();
    }

    getTime(): string {
        const now = new Date();
        const timeString = now.toLocaleTimeString([], {hour: "2-digit", minute: "2-digit"});
        const dayOfWeek = new Intl.DateTimeFormat("de", {weekday: "short"}).format(now);
        return `${timeString} - ${dayOfWeek}`;
    }

    addMessage(messageText: string, title: string = "nichts") {
        if (!messageText || messageText.trim().length === 0) {
            return; // do not add empty messages
        }
        let newMessage = this.addUserMessage(messageText, title)
        this.chatbotService.sendMessage(newMessage).subscribe((response: any) => {
            this.addBotMessages(response)
        });
        this.scrollToBottom();
    }

    addUserMessage(userMessage: string, title: string): Message {

        //extract an embeded youtube link
        this.embededLink = this.getYoutubeLinkToEmbed(userMessage);

        //If a youtube link is available, it should be clickable
        //Questions: should linkify always be called?
        if (this.embededLink != "") {
            userMessage = this.linkifyYoutube(userMessage);
            this.messageHasVideo = true;
        } else {
            this.messageHasVideo = false;
            this.embededLink = "";
        }

        let newMessage: Message = {
            text: userMessage,
            hasVideo: this.messageHasVideo,
            video: this.embededLink,
            image: "",
            time: this.getTime(),
            isUser: true,
            buttons: ""
        };
        let clonedMessage = {...newMessage};
        if (title !== "nichts") {
            clonedMessage.text = title
        }
        this.messages.push(clonedMessage);
        this.scrollToBottom();
        setTimeout(() => {
            this.isTyping = true;
            this.scrollToBottom();
        }, 900); // Add typing indicator after 0.9s
        //setTimeout(() => this.isTyping = false, 9000); // Remove typing indicator after 3s (backup)
        this.scrollToBottom();
        return newMessage
    }

    addBotMessage(botMessage: Message): void {
        this.isTyping = false; // Remove typing indicator, when bot message is received
        if (botMessage.text !== undefined) {
            botMessage.text = this.linkify(botMessage.text);
        }
        this.embededLink = this.getYoutubeLinkToEmbed(botMessage.text);

        if (this.embededLink != "") {
            botMessage.text = this.linkifyYoutube(botMessage.text);
            botMessage.hasVideo = true;
            botMessage.video = this.embededLink;
        } else {
            this.embededLink = "";
        }
        this.messages.push(botMessage);
        this.scrollToBottom();
    }

    scrollToBottom(): void {
        setTimeout(() => {
            const chatContainer = this.el.nativeElement.querySelector(".chat-window-messages");
            if (chatContainer) {
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }
        }, 100);
    }

    linkify(text: string): string {
        const urlRegex = /(https?:\/\/[^\s]+)/g;
        const wwwRegex = /(www.[^\s]+)/g;
        return text.replace(urlRegex, "<a href=\"$1\" target=\"_blank\">$1</a>")
            .replace(wwwRegex, "<a href=\"http://$1\" target=\"_blank\">$1</a>")
            .replace(/\n/g, "<br>");

    }

    // converts URLs into clickable links of an <a> tag
    // checks whether a protocol is available, if not it is added
    linkifyYoutube(text: string): string {
        const urlRegex = /(\bhttps?:\/\/\S+)|(www\.\S+)/g; //captures http and https

        return text.replace(urlRegex, (match, p1, p2) => {
            const protocol = p1 ? "" : "http://";
            const urlPart = p1 || p2;
            return `<a href="${protocol}${urlPart}" target="_blank">${urlPart}</a>`;
        });
    }

    async addBotMessages(response: any[]) {
        for (const element of response) {
            this.addBotMessage(element);
        }
        this.scrollToBottom();
    }

    handleButtonClick(button: { title: string; payload: string }): void {
        this.addMessage(button.payload, button.title)
    }

    async createFirstMessage(): Promise<string> {
        console.log("läuft")
        const firstMessage = {
            text: "Hi",
            hasVideo: false,
            video: "",
            image: "",
            time: "14:34",
            isUser: false,
            buttons: ""
        }
        this.chatbotService.sendMessage(firstMessage).subscribe((response: any) => {
            this.addBotMessages(response)
        });
        this.scrollToBottom();
        return "Hi"
        // const userId = localStorage.getItem("userid")
        // const userName = localStorage.getItem("username")
        // console.log("läuft")
        // if (userId != null) {
        //     try {
        //         const goals = await this.goalService.getGoals(parseInt(userId)).toPromise();
        //         console.log("läuft22")
        //         if (goals[0].goal != null) {
        //             return `Hi ${userName} 👋, wie gehts dir? Wie sieht es mit deinem Ziel "${goals[0].goal}" aus? 🎯`;
        //         } else {
        //             return `Hi ${userName} 👋, du hast dir noch gar kein Ziel gesetzt. Wenn du Lust hast dir ein Ziel zu setzen, dann schreib mir einfach 🎯. Wir können aber auch ein Quiz machen wenn du Lust hast!`;
        //         }
        //     } catch (error) {
        //         console.error(error);
        //         return "Es ist ein Fehler aufgetreten!";
        //     }
        // } else {
        //     return "Hi, bitte melde dich doch an!";
        // }
    }

    // searches for a youtube link and replaces it with an "embedded" link for insertion in an <iframe>
    getYoutubeLinkToEmbed(url: string): string | SafeResourceUrl {
        const youtubeRegex = /(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?(?:.*&)?v=([a-zA-Z0-9_-]+)/;
        const match = url.match(youtubeRegex);

        if (match && match[1]) {
            return this.sanitizer.bypassSecurityTrustResourceUrl(`https://www.youtube.com/embed/${match[1]}`);
        }

        return "";
    }

    public isChatOpen(): boolean {
        return this.chatbotService.isChatWindowVisible;
    }

    public toggleChat(): void {
        return this.chatbotService.toggleChatWindow();
    }

    //change the CSS class of the chat window, if the user wants to change the size of the chat window
    public changeWindowSize(): void {
        this.isFullScreen = !this.isFullScreen;
    }
}
