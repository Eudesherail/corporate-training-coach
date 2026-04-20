import { Component, EventEmitter, Output } from '@angular/core';
import {ChatService} from "../../../../api/chat/chat.service";

@Component({
  selector: 'app-emoji-fenster',
  templateUrl: './emoji-fenster.component.html',
  styleUrls: ['./emoji-fenster.component.scss']
})


export class EmojiFensterComponent {

  @Output() closeEmoji = new EventEmitter();
  
  get EmojisVisible(): boolean {
    return this.BotService.isEmojiPickerVisible;
  }
  constructor(private BotService: ChatService) {
}

  public addEmoji(event: { emoji: { native: any; }; }) {   
    this.BotService.userInput = event.emoji.native;
    this.BotService.emojiIsSelected();
  }

  onCloseClick() {
    this.closeEmoji.emit();
  }
}
