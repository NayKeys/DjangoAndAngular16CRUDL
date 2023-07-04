import App from './App.svelte';

export type RowKeys = string[];
export type RowValues = string[];

export type ApiRequest = {
	action: string;
	jwt: string;
	view_name: string;
	row: { [key: string]: string };
};
export type ApiResponse = {
	status: number;
	message: string;
  row_keys: RowKeys;
  rows: RowValues[];
};

const apiActionRequest = async function (csrfToken: string, jwt: string, action: string, viewName: string = "", keys: RowKeys, values: RowValues): Promise<{names: RowKeys, table: RowValues[]} | undefined> {
	const data = keys.reduce((obj, key, index) => {  // Converts key values to object
		obj[key] = values[index];
		return obj;
	}, {} as { [key: string]: string });
	const request: ApiRequest = {
		action: action,
		jwt: jwt,
		view_name: viewName,
		row: data,
	};
	const res = await fetch("http://localhost:8000/app/execute/", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
			"X-CSRFToken": csrfToken,
		},
		body: JSON.stringify(request),
	});
	const rows: RowValues[] = [];
	const resJson: ApiResponse = await res.json();
	if (resJson.status !== 200) {
		// If api returns error
		console.log("Error: " + resJson.message);
		return undefined;
	} else {
		return {names: resJson.row_keys, table: resJson.rows};
	}
};

export function getMeta(metaName: string) {
	const metas = document.getElementsByTagName("meta");
	for (let i = 0; i < metas.length; i++) {
		if (metas[i].getAttribute("name") === metaName) {
			return metas[i].getAttribute("content");
		}
	}
	return "";
}

export function getCookie(name: string) {
	const value = `; ${document.cookie}`;
	const parts = value.split(`; ${name}=`);
	if (parts.length === 2) return parts.pop().split(";").shift();
}

export function setCookie(name: string, value:string, hours:number) {
	let expires = "";
	if (hours) {
		const date = new Date();
		date.setTime(date.getTime() + hours * 60 * 60 * 1000);
		expires = `; expires=${date.toUTCString()}`;
	}
	document.cookie = `${name}=${value || ""}${expires}; path=/; SameSite=Lax;`;
}



const app = new App({
	target: document.body,
	props: {
	},
});

export { apiActionRequest };
export default app;