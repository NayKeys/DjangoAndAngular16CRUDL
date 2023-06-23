import App from './App.svelte';

const app = new App({
	target: document.body,
	props: {
		name: 'world'
	}
});

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

export type RequestData = {
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

let apiActionRequest = async function(action: string, data: DataRow): Promise<DataRow[]> {
  const request: RequestData = {
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
		},
		body: JSON.stringify(request),
	});
  const rows: DataRow[] = [];
  const resJson: ReferenceData[] = await res.json();
	for(const i in resJson) {
    const refData = resJson[i];
    const row: DataRow = [refData.id.toString(), refData.reference.first_name, refData.reference.last_name, refData.reference.role, refData.reference.age, refData.reference.grade, refData.reference.address]
    rows.push(row);
  } 
  return rows;
}
export { apiActionRequest };

export default app;