<script lang="ts">
  import type { RowKeys, RowValues } from './main'
  export let columnNames:RowKeys  // Prop
  export let table: RowValues[] // Prop
  export let newRow: RowValues // Prop
  export let addRow: RowValues // Prop
  export let updateRow: RowValues // Prop
  export let deleteRow: RowValues // Prop

  import DataTable, { Head, Body, Row, Cell, Label, SortValue, } from '@smui/data-table';
  import IconButton from '@smui/icon-button';

  type User = {
    id: number;
    name: string;
    username: string;
    email: string;
    website: string;
  };
  let items: User[] = [];
  let sort: keyof User = 'id';
  let sortDirection: Lowercase<keyof typeof SortValue> = 'ascending';

  if (typeof fetch !== 'undefined') {
    fetch(
      'https://gist.githubusercontent.com/hperrin/e24a4ebd9afdf2a8c283338ae5160a62/raw/dcbf8e6382db49b0dcab70b22f56b1cc444f26d4/users.json'
    )
      .then((response) => response.json())
      .then((json) => (items = json));
  }

  function handleSort() {
    items.sort((a, b) => {
      const [aVal, bVal] = [a[sort], b[sort]][
        sortDirection === 'ascending' ? 'slice' : 'reverse'
      ]();
      if (typeof aVal === 'string' && typeof bVal === 'string') {
        return aVal.localeCompare(bVal);
      }
      return Number(aVal) - Number(bVal);
    });
    items = items;
  }
</script>
<DataTable
  sortable
  bind:sort
  bind:sortDirection
  on:SMUIDataTable:sorted={handleSort}
  table$aria-label="User list"
  style="width: 100%;"
>
  <Head>
    <Row>
      <!--
        Note: whatever you supply to "columnId" is
        appended with "-status-label" and used as an ID
        for the hidden label that describes the sort
        status to screen readers.
 
        You can localize those labels with the
        "sortAscendingAriaLabel" and
        "sortDescendingAriaLabel" props on the DataTable.
      -->
      <Cell numeric columnId="id">
        <!-- For numeric columns, icon comes first. -->
        <IconButton class="material-icons">arrow_upward</IconButton>
        <Label>ID</Label>
      </Cell>
      <Cell columnId="name" style="width: 100%;">
        <Label>Name</Label>
        <!-- For non-numeric columns, icon comes second. -->
        <IconButton class="material-icons">arrow_upward</IconButton>
      </Cell>
      <Cell columnId="username">
        <Label>Username</Label>
        <IconButton class="material-icons">arrow_upward</IconButton>
      </Cell>
      <Cell columnId="email">
        <Label>Email</Label>
        <IconButton class="material-icons">arrow_upward</IconButton>
      </Cell>
      <!-- You can turn off sorting for a column. -->
      <Cell sortable={false}>Website</Cell>
    </Row>
  </Head>
  <Body>
    {#each items as item (item.id)}
      <Row>
        <Cell numeric>{item.id}</Cell>
        <Cell>{item.name}</Cell>
        <Cell>{item.username}</Cell>
        <Cell>{item.email}</Cell>
        <Cell>{item.website}</Cell>
      </Row>
    {/each}
  </Body>
</DataTable>
<table class="table">
  <tr class="row-1">
    {#each columnNames as column}
    <th class="cell">
      <div class="content">
        <div class="text lexenddeca-semi-bold-oslo-gray-20px  ">
          {column}
        </div>
      </div>
    </th>
    {/each}
  </tr>
  {#each table as row}
  <tr class="row">
    {#each row as cell}
    <th class="cell">
      <div class="content">
        <div class="text  lexenddeca-normal-geyser-24px">
          {cell}
        </div>
      </div>
    </th>
    {/each}
  </tr>
  {/each}
</table>

<style>
  .table {
    align-items: flex-start;
    align-self: stretch;
    border-radius: 4px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    position: relative;
  }
  .content {
    align-items: flex-start;
    align-self: stretch;
    display: flex;
    padding: 3px 12px;
    position: relative;
  }
  .text {
    text-align: start;
    flex: 1;
    letter-spacing: 0;
    line-height: 31.2px;
    margin-top: -1px;
    position: relative;
    white-space: nowrap;
  }
  .row-1 {
    align-items: flex-start;
    align-self: stretch;
    background-color: #ffffff00;
    display: flex;
    height: 51px;
    overflow: hidden;
    position: relative;
  }
  .row {
    align-items: flex-start;
    align-self: stretch;
    background-color: #ffffff00;
    display: flex;
    height: 46px;
    overflow: hidden;
    position: relative;
  }
  .cell {
    align-items: flex-start;
    align-self: stretch;
    background-color: var(--shark);
    border: 0px none;
    display: flex;
    flex-direction: column;
    position: relative;
    width: 250px;
    overflow: hidden;
    border-top-style: solid;
    border-top-width: 1px;
    border-right-style: solid;
    border-right-width: 1px;
  }
</style>