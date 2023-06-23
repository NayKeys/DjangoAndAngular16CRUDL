import App from './App.svelte';

export type ReferenceData = {
	id: number;
	reference: {
		first_name: string;
		last_name: string;
		role: string;
		age: string;
		grade: string;
		address: string;
	};
};

export type ApiRequest = {
	action: string;
	jwt: string;
	data: ReferenceData;
};

export type DataRow = [
	id: string,
	firstName: string,
	lastName: string,
	role: string,
	age: string,
	grade: string,
	address: string
];

export type ApiResponse = {
	status: number;
	message: string;
	data: ReferenceData[];
};

const apiActionRequest = async function(csrfToken:string, action: string, data: DataRow): Promise<DataRow[]> {
  const request: ApiRequest = {
    action: action,
    jwt: "jwt",
    data: {
      id: parseInt(data[0]),
      reference: {
        first_name: data[1],
        last_name: data[2],
        role: data[3],
        age: data[4],
        grade: data[5],
        address: data[6],
      },
    }
  }
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
    return rows;
  } else {
    for(let i = 0; i < resJson.data.length; i++) {
      const refData = resJson.data[i];
      const row: DataRow = [refData.id.toString(), refData.reference.first_name, refData.reference.last_name, refData.reference.role, refData.reference.age, refData.reference.grade, refData.reference.address]
      rows.push(row);
    }
    return rows;
  }
}

const app = new App({
	target: document.body,
	props: {
	},
});

export { apiActionRequest };
export default app;