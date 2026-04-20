/**
 * This Service handles how the date is represented in scripts i.e. ngModel.
 * Model Output: YYYY-MM-DD
 * Model Input: DD.MM.YYYY
 */
@Injectable()
export class StubuDateAdapter extends NgbDateAdapter<string> {
    readonly DELIMITER: string = "-";

    fromModel(value: string | null): NgbDateStruct | null {
        if (value) {
            const date = value.split(this.DELIMITER);
            return {
                day: parseInt(date[2], 10),
                month: parseInt(date[1], 10),
                year: parseInt(date[0], 10),
            };
        }
        return null;
    }

    toModel(date: NgbDateStruct | null): string | null {
        return date 
            ? date.year + this.DELIMITER
            + this.addLeadingZero(date.month) + this.DELIMITER 
            + this.addLeadingZero(date.day) : null;
    }
    
    addLeadingZero(value: number): string {
        if (value < 10) {
            return "0" + value;
        }
        return value.toString();
    }
    
}

/**
 * This Service handles how the date is rendered and parsed from keyboard i.e. in the bound input field.
 */
@Injectable()
export class StubuDateParserFormatter extends NgbDateParserFormatter {
    readonly DELIMITER = ".";

    parse(value: string): NgbDateStruct | null {
        if (value) {
            const date = value.split(this.DELIMITER);
            return {
                day: parseInt(date[0], 10),
                month: parseInt(date[1], 10),
                year: parseInt(date[2], 10),
            };
        }
        return null;
    }

    format(date: NgbDateStruct | null): string {
        return date 
            ? this.addLeadingZero(date.day) + this.DELIMITER
            + this.addLeadingZero(date.month) + this.DELIMITER
            + this.addLeadingZero(date.year) : "";
    }

    addLeadingZero(value: number): string {
        if (value < 10) {
            return "0" + value;
        }
        return value.toString();
    }
}

import {Component, Injectable} from "@angular/core";
import {NgbDateAdapter, NgbDateParserFormatter, NgbDateStruct} from "@ng-bootstrap/ng-bootstrap";
import {GoalService} from "../../api/goal/goal.service";
import {AlertService} from "../../_helper/alert.service";

@Component({
    selector: "app-goal-editor",
    templateUrl: "./goal-editor.component.html",
    styleUrls: ["./goal-editor.component.scss"],
    providers: [
        {provide: NgbDateAdapter, useClass: StubuDateAdapter},
        {provide: NgbDateParserFormatter, useClass: StubuDateParserFormatter},
    ],
})
export class GoalEditorComponent {
    id: number | null = null;
    goal: string | null = null;
    newGoal: string | null = null;
    startDate: string | null = null;
    endDate: string | null = null;
    goalEditMode: boolean = !!this.goal;
    updateGoal: boolean = false;
    userId: number = Number(localStorage.getItem("userid"));

    constructor(private goalService: GoalService, private alertService: AlertService) {
        this.loadGoal();
    }

    public editGoal(): void {
        // Check if the end date is in the past or invalid
        const currentDate = new Date();
        let inputEndDate: Date | null = null;
        
        if (this.endDate) {
            inputEndDate = new Date(this.endDate);
        }
        
        if (!inputEndDate || inputEndDate < currentDate) {
            this.alertService.warn('The end date is in the past or invalid.');
            return;
        }
    
        const goalData = {
            goal: this.goal,
            startDate: this.startDate,
            endDate: this.endDate,
        };
        let goalObservable;  // Observable to either handle creating or updating a goal
        
        // Corrected the logic here
        if (this.updateGoal) {
            console.log("Updating Goal");
            goalObservable = this.goalService.updateGoal(this.userId, this.id ? Number(this.id) : -1, goalData);
        } else {
            console.log("Creating Goal");
            goalObservable = this.goalService.createGoal(this.userId, goalData);
        }
    
        goalObservable.subscribe(
            // 'next' Callback: Called when the server responds successfully
            () => {
                this.alertService.info('Goal has been successfully saved.');
                this.loadGoal();  // Reload goal to reflect the changes
            },
            // 'error' Callback: Called when an error occurs
            (error) => {
                this.alertService.warn('An error occurred while saving the goal.');
            }
        );
    }
    
    

    cancelGoal(): void {
        this.loadGoal();
    }

    private loadGoal(): void {
        console.log("loadGoal");
        this.goalService.getGoals(this.userId).subscribe((goals) => {
            if (goals != null && goals != "") {
                console.log("Goal found");
                this.id = goals[0].id;
                this.goal = goals[0].goal;
                this.startDate = goals[0].startDate;
                this.endDate = goals[0].endDate;
                this.goalEditMode = true;
            } else {
                console.log("No goal found");
                this.goalEditMode = false;
                this.updateGoal = false;
            }
        });
    }
}