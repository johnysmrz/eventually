export class MenuItem {
    id: string;
    label: string;
    icon?: string;
    route?: string;
    enabled: boolean;
    children?: MenuItem[];

    constructor(params: {
        id: string;
        label: string;
        icon?: string;
        route?: string;
        enabled?: boolean;
        children?: MenuItem[];
    }) {
        this.id = params.id;
        this.label = params.label;
        this.icon = params.icon;
        this.route = params.route;
        this.enabled = params.enabled ?? true;
        this.children = params.children;
    }
}
