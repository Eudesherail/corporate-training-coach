import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Injectable} from "@angular/core";
import {Observable} from "rxjs";
import {map} from "rxjs/operators";
import {environment} from "../../../environments/environment";
import {Message} from "./message.model";

@Injectable({
    providedIn: "root"
})
export class ChatService {
    private url = `${environment.backendUrl}/api/message/`;
    public isEmojiPickerVisible: boolean = false;
    public isChatWindowVisible: boolean = false;
    public userInput: any;
    public EmojiAdd: boolean = false;
    private httpOptions = {
        headers: new HttpHeaders({
            "Content-Type": "application/json"
        })
    };

    constructor(private http: HttpClient) {
    }

    emojiIsSelected() {
        this.EmojiAdd = true;
    }

    makeEmojiVisible() {
        this.isEmojiPickerVisible = !this.isEmojiPickerVisible;
    }

    toggleChatWindow(): void {
        this.isChatWindowVisible = !this.isChatWindowVisible;
    }

    time(): string {
        const now = new Date();
        const timeString = now.toLocaleTimeString([], {hour: "2-digit", minute: "2-digit"});
        const dayOfWeek = new Intl.DateTimeFormat("de", {weekday: "short"}).format(now);
        return `${timeString} - ${dayOfWeek}`;
    }

    sendMessage(message: Message): Observable<Message[]> {
        const body = {
            message: message.text,
        };
        return this.http.post<any>(this.url, body, this.httpOptions).pipe(
            map(responses => {
                const responseMessages: Message[] = [];
                if (Array.isArray(responses)) {
                    responses.forEach((element: any) => {
                        const message: Message = {
                            text: element.message,
                            hasVideo: false,
                            video: "",
                            image: "",
                            time: this.time(),
                            isUser: false,
                            buttons: ""
                        }
                        responseMessages.push(message)
                    });
                } else {
                    console.log(responses)
                    const message: Message = {
                        text: responses.message,
                        hasVideo: false,
                        video: "",
                        image: "",
                        time: this.time(),
                        isUser: false,
                        buttons: ""
                    }
                    responseMessages.push(message)
                }
                return responseMessages;
            })
        );

    }
}
