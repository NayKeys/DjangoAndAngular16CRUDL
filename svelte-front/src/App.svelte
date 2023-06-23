<script lang="ts">
  import Table from './Table.svelte';  // From https://svelte.dev/repl/36aaf2a1807a4fed81fe6212d20bca24?version=3.25.1
  import { onMount } from 'svelte';
  type Row = [
    id: string,
    firstName: string,
    lastName: string,
    role: string,
    age: string,
    grade: string,
    address: string,
  ]
	function addRow() {
		data = [...data, [...newRow]]
		newRow = ['', "", "", "", '', '', ""]
	}
	function deleteRow(rowToBeDeleted: Row) {
		data = data.filter(row => row != rowToBeDeleted)
	}
	let columns: string[] = ["ID", "First Name", "Last Name", "Role", "Age", "Grade", "Address"]  // Idea: make this a prop sent from the backend
  
  onMount(async () => {
    // const res = await fetch('http://localhost:8000/api/execute/', {
    //   method: 'POST',
    //   headers: {
    //     'Content-Type': 'application/json',
    //   },
    //   body: JSON.stringify({
    //     action: 'fetch_all',
    //   }),
    // });
    // students = await res.json();
  });
  
  let data: Row[] = [
    ['1', "John", "Fisher", "student", '22', '1', "21 uwu sur uwu plage"],
    ['2', "Sarah", "Fisher", "student", '22', '1', "21 uwu sur uwu plage"],
    ['3', "Afshin", "Fisher", "student", '22', '1', "21 uwu sur uwu plage"]
  ]
	let newRow: Row = ['', "", "", "", '', '', ""];
</script>

<table>
	<tr>
		{#each columns as column}
			<th>{column}</th>
		{/each}
	</tr>
	
	{#each data as row}
		<tr>
			{#each row as cell}
        <td contenteditable="true" bind:innerHTML={cell} />
			{/each}
			<button on:click={() => deleteRow(row)}>X</button>
		</tr>
	{/each}

	<tr style="color: grey">
		{#each newRow as column}
			<td contenteditable="true" bind:innerHTML={column} />
		{/each}
		<button on:click={addRow}>add</button>
	</tr>

	<pre style="background: #eee">{JSON.stringify(data, null, 2)}</pre>
</table>

<style>
	tr td:focus {
		background: #eee;
	}
</style>