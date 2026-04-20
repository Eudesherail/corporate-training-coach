import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-chat-header',
  templateUrl: './chat-header.component.html',
  styleUrls: ['./chat-header.component.scss']
})
export class ChatHeaderComponent {
  title = 'Study Buddy';
  avatarIcon: string;

  @Output() closeChat = new EventEmitter();
  @Output() changeSize = new EventEmitter();
  
  constructor() {
    const avatarName = localStorage.getItem("avatarName") ?? "Mensch-1";
    this.avatarIcon = `assets/avatars/${avatarName}-Kopf.png`;
  }

  onCloseClick() {
    this.closeChat.emit();
  }

  changeWindowSize() {
    this.changeSize.emit();
  }
}
