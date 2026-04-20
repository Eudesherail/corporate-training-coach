import {NgFor, NgIf} from "@angular/common";
import {Component, EventEmitter, Input, OnChanges, Output, SimpleChanges} from "@angular/core";
import {NgbCarouselModule, NgbSlideEvent} from "@ng-bootstrap/ng-bootstrap";

@Component({
    selector: "app-avatar-carousel",
    templateUrl: "./avatar-carousel.component.html",
    standalone: true,
    imports: [
        NgbCarouselModule,
        NgIf, NgFor
    ],
    styleUrls: ["./avatar-carousel.component.scss"]
})
export class AvatarCarouselComponent implements OnChanges {
    images: string[] = ["Mensch-1", "Mensch-2", "Mensch-3", "Robot-1", "Robot-2", "Robot-3", "Android-1", "Android-2", "Android-3"]
        .map((n) => `assets/avatars/${n}.png`);
    activeId: string = "" + 0;

    @Input()
    avatarName: string = "Mensch-1";

    @Output()
    avatarNameChange: EventEmitter<string> = new EventEmitter<string>();

    constructor() {
    }

    public onSlide(slideEvent: NgbSlideEvent): void {
        const imageId = parseInt(slideEvent.current.replace("slideId_", ""), 10)
        this.avatarName = this.images[imageId].replace("assets/avatars/", "").replace(".png", "");
        this.activeId = "" + imageId;
        this.avatarNameChange.emit(this.avatarName);
    }

    public ngOnChanges(changes: SimpleChanges): void {
        if (changes["avatarName"]) {
            this.activeId = "" + this.images.findIndex((n) => n.includes(changes["avatarName"].currentValue));
        }
    }
}
