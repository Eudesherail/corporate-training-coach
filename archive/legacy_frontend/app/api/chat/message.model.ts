import { SafeResourceUrl } from '@angular/platform-browser'

export interface Message {
  text: string;
  time: string;
  hasVideo: boolean;
  video: string | SafeResourceUrl;
  image: string;
  isUser: boolean;
  buttons: any;
}
