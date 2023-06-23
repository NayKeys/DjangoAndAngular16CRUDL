<script>
  import { onMount } from 'svelte';
  let students = [];
  let selectedStudent = null;

  onMount(async () => {
    const res = await fetch('http://localhost:8000/api/execute/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        action: 'fetch_all',
        
      }),
    });
    students = await res.json();
  });

  function selectStudent(student) {
    selectedStudent = student;
  }

  async function saveStudent() {
    // Add or update a student
    const action = selectedStudent.id ? 'update' : 'insert';
    const res = await fetch('http://localhost:8000/api/execute', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        action,
        data: { student: selectedStudent },
      }),
    });
    students = await res.json();
  }

  async function deleteStudent() {
    // Delete a student
    const res = await fetch('http://localhost:8000/api/execute', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        action: 'delete',
        data: { id: selectedStudent.id },
      }),
    });
    students = await res.json();
  }
</script>

<table>
  <thead>
    <tr>
      <th>ID</th>
      <th>First Name</th>
      <th>Last Name</th>
      <th>Age</th>
      <th>Grade</th>
    </tr>
  </thead>
  <tbody>
    {#each students as student (student.id)}
      <tr on:click={() => selectStudent(student)}>
        <td>{student.id}</td>
        <td>{student.first_name}</td>
        <td>{student.last_name}</td>
        <td>{student.age}</td>
        <td>{student.grade}</td>
      </tr>
    {/each}
  </tbody>
</table>

{#if selectedStudent}
  <div>
    <input bind:value={selectedStudent.first_name} placeholder="First Name" />
    <input bind:value={selectedStudent.last_name} placeholder="Last Name" />
    <input bind:value={selectedStudent.age} type="number" placeholder="Age" />
    <input bind:value={selectedStudent.grade} type="number" placeholder="Grade" />
    <button on:click={saveStudent}>Save</button>
    <button on:click={deleteStudent}>Delete</button>
  </div>
{/if}