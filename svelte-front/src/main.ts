import App from './App.svelte';

export type ReferenceData = {
	id: number;
  username: string;
	reference: {
		first_name: string;
		last_name: string;
		role: string;
		age: string;
		grade: string;
		homeaddress: string;
	};
};

export type ApiRequest = {
	action: string;
	jwt: string;
	data: ReferenceData;
};

export type DataRow = [
	id: string,
  username: string,
	firstName: string,
	lastName: string,
	role: string,
	age: string,
	grade: string,
	homeaddress: string
];

export type ApiResponse = {
	status: number;
	message: string;
	data: ReferenceData[];
};

const apiActionRequest = async function(csrfToken:string, action: string, data: DataRow): Promise<DataRow[] | undefined> {
  const request: ApiRequest = {
		action: action,
		jwt: "jwt",
		data: {
			id: parseInt(data[0]),
      username: data[1],
			reference: {
				first_name: data[2],
				last_name: data[3],
				role: data[4],
				age: data[5],
				grade: data[6],
				homeaddress: data[7],
			},
		},
	};
  const res = await fetch("http://localhost:8000/api/execute/", {
		method: "POST",
		headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
		},
		body: JSON.stringify(request),
	});
  const rows: DataRow[] = [];
  const resJson: ApiResponse = await res.json();
  if (resJson.status !== 200) {  // If api returns error
    console.log("Error: " + resJson.message);
    return undefined;
  } else {
    if (resJson.data != undefined) {
      for(let i = 0; i < resJson.data.length; i++) {
        const refData = resJson.data[i];
        const row: DataRow = [refData.id.toString(), refData.username, refData.reference.first_name, refData.reference.last_name, refData.reference.role, refData.reference.age, refData.reference.grade, refData.reference.homeaddress];
        rows.push(row);
      }
    }
    return rows;
  }
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