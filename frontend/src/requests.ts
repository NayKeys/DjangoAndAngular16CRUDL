export type RowKeys = string[];
export type RowValues = string[];

const csrfToken = getMeta("csrf-token");
let jwt = getCookie("jwt");

export function refreshToken() {
  jwt = getCookie("jwt");
}

refreshToken()

export type ApiActionRequestBody = {
	action: string;
	view_name: string;
	row: { [key: string]: string };
};
export type ApiActionResponseBody = {
	status: number;
	message: string;
	row_keys: RowKeys;
	rows: RowValues[];
};

export async function apiActionRequest(action: string, viewName: string = "", keys: RowKeys, values: RowValues): Promise<{ names: RowKeys; table: RowValues[] } | undefined> {
	const data = keys.reduce((obj, key, index) => {
		// Converts key values to object
		obj[key] = values[index];
		return obj;
	}, {} as { [key: string]: string });
	const request: ApiActionRequestBody = {
		action: action,
		view_name: viewName,
		row: data,
	};
	const res = await fetch(window.location.origin+"/app/execute/", {
    method: "POST",
		headers: {
      "token": jwt,
			"Content-Type": "application/json",
			"X-CSRFToken": csrfToken,
		},
		body: JSON.stringify(request),
	});
	const rows: RowValues[] = [];
	const resJson: ApiActionResponseBody = await res.json();
	if (resJson.status !== 200) {
		// If api returns error
		console.log("Error: " + resJson.message);
		return undefined;
	} else {
		return { names: resJson.row_keys, table: resJson.rows };
	}
}

export type View = {
	method: string;
	database_url: string;
	table_name: string | undefined;
	identifier_name: string | undefined;
};
export type ViewList = {};
export type TreeNode<T> = T | TreeNode<T>[];
export type ViewTree = {
	has_view_sets: boolean;
	root: TreeNode<View>;
};

export async function apiTreeRequest(): Promise<ViewTree | undefined> {
	let res = await fetch(window.location.origin+"/app/viewtree/", {
		method: "GET",
		headers: {
			"Content-Type": "application/json",
			"X-CSRFToken": csrfToken,
		},
	});
	return await res.json();
}

export function getMeta(metaName: string) {
	const metas = document.getElementsByTagName("meta");
	for (let i = 0; i < metas.length; i++) {
		if (metas[i].getAttribute("name") === metaName) {
			return metas[i].getAttribute("content");
		}
	}
	return "";
}

export async function getUserPermissions() {
	const response = await fetch("/user/permissions/", {
		method: "GET",
		headers: {
			"X-CSRFToken": csrfToken,
      "token": jwt,
			"Content-Type": "application/json",
		},
	});
	if (response.status == 200) {
		return response;
	}
	return null;
}

export function getCookie(name: string) {
	const value = `; ${document.cookie}`;
	const parts = value.split(`; ${name}=`);
	if (parts.length === 2) return parts.pop().split(";").shift();
}

export function setCookie(name: string, value: string, hours: number) {
	let expires = "";
	if (hours) {
		const date = new Date();
		date.setTime(date.getTime() + hours * 60 * 60 * 1000);
		expires = `; expires=${date.toUTCString()}`;
	}
	document.cookie = `${name}=${value || ""}${expires}; path=/; SameSite=Lax;`;
}
