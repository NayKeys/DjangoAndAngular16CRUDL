<script lang="ts">
  import InputFieldsList from "./InputFieldsList.svelte";
  import Button from "./Button.svelte";
  import type { RowKeys, RowValues } from './requests';
  import { TextInput, TextInputSkeleton } from "carbon-components-svelte";

  
  export let addRow: (keys: RowKeys, newRow: RowValues) => void;
  export let hideCreationFrame: (e: any) => void;
  export let columnNames: RowKeys = [];

  let oldRow: RowValues = [];
  let newRow: RowValues = [];
  let id: string;

  const show = true;  // futur use
</script>

<div class="edit-frame-container {show ? 'shown' : 'hidden'}">
  {#if show}
    <div class="flex-col flex">
      <div class="flex-row flex">
        <div on:click={hideCreationFrame} on:keypress={() => (true)}>
          <Button fill={true} text="cancel" width={50} confirmation="Are you sure you want to cancel creation ?" >
            <svg xmlns="http://www.w3.org/2000/svg" class="button-vector" width="50" height="40" fill="none" viewBox="0 0 64 53">
              <path d="M46.171 52.733H26.484a16.858 16.858 0 0 1-12.451-5.507L3.69 35.859c-4.921-5.39-4.921-13.535 0-18.955L14.033 5.537A16.778 16.778 0 0 1 26.483 0h19.688c9.287 0 16.845 7.558 16.845 16.845v19.043c0 9.287-7.558 16.845-16.845 16.845ZM26.484 4.394a12.492 12.492 0 0 0-9.2 4.073L6.915 19.863a9.671 9.671 0 0 0 0 13.037l10.341 11.367a12.492 12.492 0 0 0 9.2 4.072H46.17c6.855 0 12.45-5.596 12.45-12.451V16.845c0-6.855-5.595-12.45-12.45-12.45H26.484Z"/>
              <path d="M43.24 35.8a2.173 2.173 0 0 1-1.552-.644L27.216 20.654a2.21 2.21 0 0 1 0-3.105 2.21 2.21 0 0 1 3.105 0L44.794 32.05c.85.85.85 2.256 0 3.106-.44.44-.996.644-1.553.644Z"/>
              <path d="M28.768 35.8a2.173 2.173 0 0 1-1.552-.644 2.21 2.21 0 0 1 0-3.106l14.472-14.472a2.21 2.21 0 0 1 3.106 0c.85.85.85 2.256 0 3.105L30.32 35.156c-.44.44-.996.644-1.553.644Z"/>
            </svg>
          </Button>
        </div>
        <div class="save-button">
          <Button onClick={() => addRow((id ? columnNames : columnNames.slice(1)), (id ? [id, ...newRow] : newRow))} fill={false} width={40} text="add" confirmation="Are you sure you want to create this new element ?">
            <svg class="button-vector" width="40" height="40" viewBox="0 0 43 43" xmlns="http://www.w3.org/2000/svg">
              <path d="M13.6807 21.5L19.1992 27.0185L30.2557 15.9816M16.1178 41H27.8178C37.5678 41 41.4678 37.1 41.4678 27.35V15.65C41.4678 5.9 37.5678 2 27.8178 2H16.1178C6.36777 2 2.46777 5.9 2.46777 15.65V27.35C2.46777 37.1 6.36777 41 16.1178 41Z" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </Button>
        </div>
      </div>
      <h1 class="title valign-text-middle">Create new element</h1>
    </div>
    <div id="edit-inputs" class="frame-31 frame">
      <TextInput
        warn
        disabled={true}
        warnText="This field is supposed to be element's unique identifier and should not be given by the user."
        labelText={columnNames[0]}
        placeholder="Enter {columnNames[0]} ..."
        bind:value={id}
      />
      <InputFieldsList disabled={false} labels={columnNames.slice(1)} initialValues={[]} bind:values={newRow}/>
    </div>
  {/if}
</div>

<style>
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
    letter-spacing: 0;
    line-height: normal;
  }
</style>