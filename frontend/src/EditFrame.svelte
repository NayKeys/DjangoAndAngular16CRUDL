<script lang="ts">
  import InputFieldsList from "./InputFieldsList.svelte";
  import Button from "./Button.svelte";
  import type { RowKeys, RowValues } from './requests';
  
  export let oldRow: RowValues = [];
  export let columnNames: RowKeys = [];
  export let hideEditFrame: () => void;
  export let updateRow: (oldRow: RowValues, newRow: RowValues) => void;
  export let deleteRows: (rows: RowValues[]) => void;

  let newRow: RowValues = [];
  let show = oldRow.length > 0;
</script>

<div class="edit-frame-container {show ? 'shown' : 'hidden'}">
  {#if show}
    <div class="flex-col flex">
      <div class="flex-row flex">
        <div>
          <Button onClick={hideEditFrame} fill={true} text="close" width={40} >
            <svg class="button-vector" width="42" height="42" viewBox="0 0 42 42" xmlns="http://www.w3.org/2000/svg">
              <path d="M26.5201 41.4679H14.9477C4.47467 41.4679 0 36.9932 0 26.5201V14.9477C0 4.47467 4.47467 0 14.9477 0H26.5201C36.9932 0 41.4679 4.47467 41.4679 14.9477V26.5201C41.4679 36.9932 37.0125 41.4679 26.5201 41.4679ZM14.9477 2.89311C6.05624 2.89311 2.89311 6.05624 2.89311 14.9477V26.5201C2.89311 35.4116 6.05624 38.5748 14.9477 38.5748H26.5201C35.4116 38.5748 38.5748 35.4116 38.5748 26.5201V14.9477C38.5748 6.05624 35.4116 2.89311 26.5201 2.89311H14.9477Z"/>
              <path d="M13.0185 41.4679C12.2277 41.4679 11.572 40.8121 11.572 40.0213V1.44658C11.572 0.655801 12.2277 3.05176e-05 13.0185 3.05176e-05C13.8093 3.05176e-05 14.4651 0.655801 14.4651 1.44658V40.0213C14.4651 40.8121 13.8286 41.4679 13.0185 41.4679Z"/>
              <path d="M26.518 27.1179C26.1515 27.1179 25.7851 26.9829 25.4957 26.6936L20.5582 21.756C19.9988 21.1967 19.9988 20.2709 20.5582 19.7116L25.4957 14.7739C26.0551 14.2146 26.9809 14.2146 27.5402 14.7739C28.0995 15.3333 28.0995 16.2591 27.5402 16.8184L23.6442 20.7338L27.5595 24.6491C28.1188 25.2085 28.1188 26.1343 27.5595 26.6936C27.2702 26.9829 26.9037 27.1179 26.518 27.1179Z"/>
            </svg>
          </Button>
        </div>
        <div class="save-button">
          <Button onClick={() => updateRow(oldRow, newRow)} fill={false} width={40} text="save" confirmation="Are you sure you want to update this element ?">
            <svg class="button-vector" width="43" height="43" viewBox="0 0 43 43" xmlns="http://www.w3.org/2000/svg">
              <path d="M13.6807 21.5L19.1992 27.0185L30.2557 15.9816M16.1178 41H27.8178C37.5678 41 41.4678 37.1 41.4678 27.35V15.65C41.4678 5.9 37.5678 2 27.8178 2H16.1178C6.36777 2 2.46777 5.9 2.46777 15.65V27.35C2.46777 37.1 6.36777 41 16.1178 41Z" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </Button>
        </div>
      </div>
      {#if columnNames.length === 0}
        <h1 class="title valign-text-middle">Edit Element</h1>
      {:else}
        <h1 class="title valign-text-middle">{columnNames[0] + ': ' + oldRow[0]}</h1>
      {/if}
    </div>
    <div id="edit-inputs" class="frame-31 frame">
      <InputFieldsList disabled={oldRow.length == 0} labels={columnNames} initialValues={oldRow} bind:values={newRow}/>
    </div>
    <Button onClick={() => deleteRows([oldRow])} class="delete-button" width={37} text="Delete" fill={true} confirmation="Are you sure you want to delete this element ? This action is irreversible.">
      <svg class="button-vector" xmlns="http://www.w3.org/2000/svg" width="37" height="37" fill="none" viewBox="0 0 64 76">
        <path d="M27.647.583 7.127 8.269C3.208 9.76 0 14.388 0 18.604v30.22c0 3.023 1.977 7.015 4.403 8.806l20.52 15.334c3.62 2.724 9.551 2.724 13.17 0l20.52-15.334c2.426-1.828 4.403-5.783 4.403-8.805V18.604c0-4.179-3.208-8.843-7.126-10.298L35.37.62C33.28-.2 29.773-.2 27.647.583Z" opacity=".4"/>
        <path d="m41.526 41.063-5.933-5.932 5.783-5.783a2.815 2.815 0 0 0 0-3.955 2.815 2.815 0 0 0-3.954 0l-5.783 5.783-5.933-5.932a2.815 2.815 0 0 0-3.954 0 2.815 2.815 0 0 0 0 3.955l5.932 5.932-6.12 6.12a2.815 2.815 0 0 0 0 3.954c.56.56 1.27.82 1.978.82.71 0 1.418-.26 1.978-.82l6.119-6.119 5.932 5.932c.56.56 1.268.821 1.977.821a2.77 2.77 0 0 0 1.978-.82c1.082-1.12 1.082-2.873 0-3.956Z"/>
      </svg>
    </Button>
  {/if}
</div>

<style>
  :global(#edit-inputs .bx--form-item) {
    width: 100%;
  }
  :global(#edit-inputs .bx--label) {
    font-family: var(--font-family-lexend_deca);
    font-size: 16px;
    color: var(--darkcontroltext);
  }
  :global(#edit-inputs .bx--text-input:focus) {
    outline: 2px solid var(--specialcolor);
    outline-offset: -2px;
  }
  :global(#edit-inputs .bx--text-input) {
    width: 100%;
    font-family: var(--font-family-lexend_deca);
    font-size: 18px;
    color: var(--whitetext);
    border: 2px solid var(--lightseperation) ;
    outline: none;
    border-radius: 6px;
    background-color: var(--lightbackground);
  }
  .edit-frame-container {
    display: flex;
    flex-direction: column;
    gap: 30px;
  }
  .shown {
    display: flex;
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
    margin-right: 6.53px;
    min-width: 671px;
    justify-content: space-between;
  }
  .flex-col {
    flex-direction: column;
    gap: 29px;
    width: 100%;
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
  .title {
    color: var(--oslo-gray);
    font-family: var(--font-family-lexend_deca);
    font-size: var(--font-size-s);
    font-weight: 400;
    height: 60px;
    width: 100%;
    letter-spacing: 0;
    line-height: normal;
    min-width: 263px;
  }
</style>