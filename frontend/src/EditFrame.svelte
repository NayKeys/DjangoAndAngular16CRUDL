<script lang="ts">
  import { TextInput, TextInputSkeleton } from "carbon-components-svelte";
  import Button from "./Button.svelte";
  import type { RowKeys, RowValues } from './requests';
  
  export let selectedData: RowValues[] = [];
  export let columnNames: RowKeys = [];
  export let hideEditFrame: (e: any) => void;

  let show = selectedData.length > 0;
  let editableData: RowValues = selectedData[0];
</script>

<div class={show ? 'shown' : 'hidden'}>
  {#if show}
    <div class="flex-row flex">
      <div class="flex-col flex">
        <div on:click={hideEditFrame} on:keypress={() => (true)}>
          <Button fill={true} width={40} >
            <svg class="button-vector" width="42" height="42" viewBox="0 0 42 42" xmlns="http://www.w3.org/2000/svg">
              <path d="M26.5201 41.4679H14.9477C4.47467 41.4679 0 36.9932 0 26.5201V14.9477C0 4.47467 4.47467 0 14.9477 0H26.5201C36.9932 0 41.4679 4.47467 41.4679 14.9477V26.5201C41.4679 36.9932 37.0125 41.4679 26.5201 41.4679ZM14.9477 2.89311C6.05624 2.89311 2.89311 6.05624 2.89311 14.9477V26.5201C2.89311 35.4116 6.05624 38.5748 14.9477 38.5748H26.5201C35.4116 38.5748 38.5748 35.4116 38.5748 26.5201V14.9477C38.5748 6.05624 35.4116 2.89311 26.5201 2.89311H14.9477Z"/>
              <path d="M13.0185 41.4679C12.2277 41.4679 11.572 40.8121 11.572 40.0213V1.44658C11.572 0.655801 12.2277 3.05176e-05 13.0185 3.05176e-05C13.8093 3.05176e-05 14.4651 0.655801 14.4651 1.44658V40.0213C14.4651 40.8121 13.8286 41.4679 13.0185 41.4679Z"/>
              <path d="M26.518 27.1179C26.1515 27.1179 25.7851 26.9829 25.4957 26.6936L20.5582 21.756C19.9988 21.1967 19.9988 20.2709 20.5582 19.7116L25.4957 14.7739C26.0551 14.2146 26.9809 14.2146 27.5402 14.7739C28.0995 15.3333 28.0995 16.2591 27.5402 16.8184L23.6442 20.7338L27.5595 24.6491C28.1188 25.2085 28.1188 26.1343 27.5595 26.6936C27.2702 26.9829 26.9037 27.1179 26.518 27.1179Z"/>
            </svg>
          </Button>
        </div>
        {#if columnNames.length === 0}
          <h1 class="title valign-text-middle">Edit Element</h1>
        {:else}
          <h1 class="title valign-text-middle">{columnNames[0] + ': ' + editableData[0]}</h1>
        {/if}
      </div>
      <div class="save-button">
        <Button fill={false} width={40} text="save">
          <svg class="button-vector" width="43" height="43" viewBox="0 0 43 43" xmlns="http://www.w3.org/2000/svg">
            <path d="M13.6807 21.5L19.1992 27.0185L30.2557 15.9816M16.1178 41H27.8178C37.5678 41 41.4678 37.1 41.4678 27.35V15.65C41.4678 5.9 37.5678 2 27.8178 2H16.1178C6.36777 2 2.46777 5.9 2.46777 15.65V27.35C2.46777 37.1 6.36777 41 16.1178 41Z" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </Button>
      </div>
    </div>
    <div id="edit-inputs" class="frame-31 frame">
      <!-- <TextInput
        warn
        warnText="Your user name is different from your log in ID."
        labelText="User name"
        placeholder="Enter user name..."
      />
      <TextInput disabled labelText="User name" placeholder="Enter user name..." />
      <TextInputSkeleton hideLabel /> -->
      {#if columnNames.length === 0}
        {#each {length: 3} as _, i}
          <TextInputSkeleton hideLabel />
        {/each}
      {:else}
        {#if selectedData.length === 0}
          {#each selectedData as column}
            <TextInputSkeleton hideLabel />
          {/each}
        {:else}
          {#each {length: columnNames.length} as _, i}
            <TextInput
              labelText={columnNames[i]}
              placeholder={`Edit ${columnNames[i]} ...`}
              value={editableData[i]}
            />
          {/each}
        {/if}
      {/if}
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
  .delete-button {
    align-items: flex-start;
    display: flex;
    gap: 11px;
    position: relative;
    width: fit-content;
  }
  .vector-3 {
    margin-bottom: -1.5px;
    margin-left: -1.5px;
    margin-top: -1.5px;
    position: relative;
  }
  .vector-2 {
    height: 42.53px;
    min-width: 37px;
  }
  .delete-text-container {
    align-items: flex-start;
    align-self: stretch;
    display: flex;
    flex-direction: column;
    gap: 10px;
    justify-content: space-around;
    position: relative;
    width: fit-content;
  }
  .delete {
    color: #94302a;
    font-family: var(--font-family-lexend_deca);
    font-size: var(--font-size-l);
    font-weight: 400;
    letter-spacing: 0;
    line-height: normal;
    position: relative;
    width: fit-content;
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