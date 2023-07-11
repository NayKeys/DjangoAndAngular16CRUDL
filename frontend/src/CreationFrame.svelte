<script lang="ts">
  import InputFieldsList from "./InputFieldsList.svelte";
  import Button from "./Button.svelte";
  import type { RowKeys, RowValues } from './requests';
  
  export let addRow: (newRow: RowValues) => void;
  export let hideCreationFrame: (e: any) => void;
  export let columnNames: RowKeys = [];

  let oldRow: RowValues = [];
  let newRow: RowValues = [];

  const show = true;  // futur use
</script>

<div class={show ? 'shown' : 'hidden'}>
  {#if show}
    <div class="flex-row flex">
      <div class="flex-col flex">
        <div on:click={hideCreationFrame} on:keypress={() => (true)}>
          <Button fill={true} text="cancel" width={40} >
          </Button>
        </div>
        {#if columnNames.length === 0}
          <h1 class="title valign-text-middle">Edit Element</h1>
        {:else}
          <h1 class="title valign-text-middle">{columnNames[0] + ': ' + oldRow[0]}</h1>
        {/if}
      </div>
      <div class="save-button">
        <Button onClick={() => addRow(newRow)} fill={false} width={40} text="add">
          <svg class="button-vector" width="43" height="43" viewBox="0 0 43 43" xmlns="http://www.w3.org/2000/svg">
            <path d="M13.6807 21.5L19.1992 27.0185L30.2557 15.9816M16.1178 41H27.8178C37.5678 41 41.4678 37.1 41.4678 27.35V15.65C41.4678 5.9 37.5678 2 27.8178 2H16.1178C6.36777 2 2.46777 5.9 2.46777 15.65V27.35C2.46777 37.1 6.36777 41 16.1178 41Z" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </Button>
      </div>
    </div>
    <div id="edit-inputs" class="frame-31 frame">
      <InputFieldsList disabled={false} labels={columnNames} initialValues={[]} bind:values={newRow}/>
    </div>
  {/if}
</div>

<style>
  .shown {
    display: block;
  }
  .hidden {
    display: none;
  }
  .frame-31 {
    flex-direction: column;
    gap: 30px;
    width: 678px;
  }
  .frame {
    align-items: flex-start;
    display: flex;
    position: relative;
  }
  .valign-text-middle {
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  .flex-row {
    gap: 303px;
    height: 130px;
    margin-right: 6.53px;
    min-width: 671px;
  }
  .flex {
    align-items: flex-start;
    display: flex;
  }
  .save-button {
    align-items: flex-start;
    display: flex;
    gap: 8px;
    position: relative;
    width: fit-content;
  }
  .flex-col {
    flex-direction: column;
    gap: 29px;
    min-height: 130px;
    width: 263px;
  }
  .title {
    color: var(--oslo-gray);
    font-family: var(--font-family-lexend_deca);
    font-size: var(--font-size-s);
    font-weight: 400;
    height: 60px;
    letter-spacing: 0;
    line-height: normal;
    min-width: 263px;
  }
</style>