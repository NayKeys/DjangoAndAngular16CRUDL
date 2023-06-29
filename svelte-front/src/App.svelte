<script lang="ts">
  // From https://svelte.dev/repl/36aaf2a1807a4fed81fe6212d20bca24?version=3.25.1
  import { onMount } from 'svelte';
  import type { DataRow } from './main'
  import { apiActionRequest } from './main';
  import Login from './Login.svelte';
  import { getMeta, getCookie } from './main'
  import { auth } from './authentification'
  /* Notes:
  When update fails, the row is not updated in the backend, but the frontend is updated
  No undo button yet

  */


  const csrfToken = getMeta('csrf-token');
  const jwt = getCookie('jwt');
	function addRow() {
    apiActionRequest(csrfToken, jwt, 'create', newRow).then((res) => {
      if (res != undefined) {
        data = [...data, [...newRow]]
        console.log("res :", res)
      }
    })
	}
	function deleteRow(rowToBeDeleted: DataRow) {
    apiActionRequest(csrfToken, jwt, 'remove', rowToBeDeleted).then((res) => {
      if (res != undefined) {
        data = data.filter(row => row != rowToBeDeleted)
        console.log("res :", res)
      }
    })
	}
  function updateRow(rowToBeEdited: DataRow) {
    apiActionRequest(csrfToken, jwt, 'update', rowToBeEdited).then((res) => {
      if (res != undefined) {
        console.log("res :", res)
      }
    })
  }
	let columns: string[] = ["ID", "username", "First Name", "Last Name", "Role", "Age", "Grade", "Address"]  // i dea: make this a prop sent from the backend

  onMount(async () => {
    await auth()
    apiActionRequest(csrfToken, jwt, 'fetch_all', ["", "", "", "", "student", "", "", ""]).then((res) => {
      data = res;
      console.log("res :", res)
    })
  });
  let data: DataRow[] = [
    ['1', "johnfish22", "John", "Fisher", "student", '22', '1', "21 uwu sur uwu plage"],
    ['2', "sarahfis24", "Sarah", "Fisher", "student", '22', '1', "21 uwu sur uwu plage"],
    ['3', "afshinfi54", "Afshin", "Fisher", "student", '22', '1', "21 uwu sur uwu plage"]
  ]
	let newRow: DataRow = ['', "", "", "", "", '', '', ""];
</script>

<Login />
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
      <button on:click={() => updateRow(row)}>save changes</button>
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