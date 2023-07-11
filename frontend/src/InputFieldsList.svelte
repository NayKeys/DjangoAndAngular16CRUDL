<script lang="ts">
  import { TextInput, TextInputSkeleton } from "carbon-components-svelte";

  export let labels: string[] = [];
  export let initialValues: string[] = [];
  export let values: string[] = [];
  export let disabled: boolean = false;

  if (initialValues.length === 0) {
    values = new Array(initialValues.length).fill("");
  } else {
    values = initialValues;
  }
</script>

<!-- <TextInput
  warn
  warnText="Your user name is different from your log in ID."
  labelText="User name"
  placeholder="Enter user name..."
/>
<TextInput disabled labelText="User name" placeholder="Enter user name..." />
<TextInputSkeleton hideLabel /> -->
{#if labels.length === 0}
  {#each {length: 3} as _, i}
    <TextInputSkeleton hideLabel />
  {/each}
{:else}
  {#if disabled}
    {#each labels as column}
      <TextInputSkeleton hideLabel />
    {/each}
  {:else}
    {#each {length: labels.length} as _, i}
      <TextInput
        labelText={labels[i]}
        placeholder={`Edit ${labels[i]} ...`}
        value={values[i]}
      />
    {/each}
  {/if}
{/if}

<style>

</style>