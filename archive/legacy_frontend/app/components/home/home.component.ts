import {Component, OnInit} from "@angular/core";
import {GoalService} from "src/app/api/goal/goal.service";
import {ChatService} from "../../api/chat/chat.service";
@Component({
    selector: "app-home",
    templateUrl: "./home.component.html",
    styleUrls: ["./home.component.scss"]
})
export class HomeComponent implements OnInit {
    showFirstTimeMessage: boolean = true;
    username: string | null = localStorage.getItem("username");
    goal: string | null = "Den Stoff der verpassten Vorlesungen nachholen in Mathe.";
    endDate: string | null = null;
    daysLeft: number | null = null;
    userId: any = localStorage.getItem("userid");
    avatarName: string;
    

    constructor(private goalService: GoalService, private chatbotService: ChatService) {
        this.avatarName = localStorage.getItem("avatarName") ?? "Mensch-1";
    }

    ngOnInit(): void {
        this.goalService.getGoals(this.userId).subscribe((goals) => {
            if (goals[0].goal != null) {
                this.goal = goals[0].goal;
                this.endDate = goals[0].endDate;
                this.calculateDaysLeft();
                this.showFirstTimeMessage = false;
            }
        });
        console.log("userid: " + this.userId);
        console.log("avatarname: " + this.avatarName);
        console.log("username: " + this.username);
    }

    calculateDaysLeft(): void {
        if (this.endDate) {
            const currentDate = new Date();
            const endDate = new Date(this.endDate);
            const timeDifference = endDate.getTime() - currentDate.getTime();
            this.daysLeft = Math.ceil(timeDifference / (1000 * 60 * 60 * 24));
        }
    }

    public openChat(): void {
        this.chatbotService.toggleChatWindow();
    }
}
