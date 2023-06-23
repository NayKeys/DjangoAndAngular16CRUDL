<script lang="ts">
  import Table from './Table.svelte';  // From https://svelte.dev/repl/36aaf2a1807a4fed81fe6212d20bca24?version=3.25.1
  import { onMount } from 'svelte';
  import type { DataRow } from './main'
	function addRow() {
		data = [...data, [...newRow]]
		newRow = ['', "", "", "", '', '', ""]
	}
	function deleteRow(rowToBeDeleted: DataRow) {

		data = data.filter(row => row != rowToBeDeleted)
	}
  function update(rowToBeEdited: DataRow) {
    console.log(data)
  }
	let columns: string[] = ["ID", "First Name", "Last Name", "Role", "Age", "Grade", "Address"]  // i dea: make this a prop sent from the backend

  import { apiActionRequest } from './main';
  onMount(async () => {
    apiActionRequest('fetch_all', ["", "", "", "student", "", "", ""]).then((res) => {
      data = res;
    })
  });
  let data: DataRow[] = [
    ['1', "John", "Fisher", "student", '22', '1', "21 uwu sur uwu plage"],
    ['2', "Sarah", "Fisher", "student", '22', '1', "21 uwu sur uwu plage"],
    ['3', "Afshin", "Fisher", "student", '22', '1', "21 uwu sur uwu plage"]
  ]
	let newRow: DataRow = ['', "", "", "", '', '', ""];
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
      <button on:click={() => update(row)}>save changes</button>
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