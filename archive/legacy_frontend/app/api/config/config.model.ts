export class Config {
    username: string;
    avatarname: string;
    token: string;

    constructor(username: string, avatarname: string, token: string) {
        this.username = username;
        this.avatarname = avatarname;
        this.token = token;
    }
}