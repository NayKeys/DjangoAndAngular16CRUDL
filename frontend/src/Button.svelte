<script lang="ts">
  export let width:number = 100;
  export let text:string = "";
  export let fill:boolean = true;
  export let textHeight:number = undefined;
  export let onClick:() => void = () => {}
</script>

<div class={"button "+$$restProps.class || ''} on:click={onClick} on:keypress>
  <div class={fill ? 'button-vector-fill' : 'button-vector-stroke'}>
    <slot class="button-vector"/>
  </div>
  <h4 class="button-label" style="line-height: {textHeight ? textHeight : width/2}px; font-size: {textHeight ? textHeight : width/1.5}px">{text}</h4>
</div>

<style>
  :global(.button:hover) {
    cursor: pointer;
  }
  /* :global(.button):active {
    background-color: var(--darkcontrol);
  } */
  :global(.button:hover) .button-label {
    color: var(--whitetext);
  }
  :global(.button:active) .button-label {
    color: var(--specialcolor);
  }
  .button-vector-stroke :global(.button-vector) {
    stroke: var(--darkcontroltext);
  }
  :global(.button:hover) .button-vector-stroke :global(.button-vector) {
    stroke: var(--whitetext);
  }
  :global(.button:active) .button-vector-stroke :global(.button-vector) {
    stroke: var(--specialcolor);
  }
  .button-vector-fill :global(.button-vector) {
    fill: var(--darkcontroltext);
  }
  .button:hover .button-vector-fill :global(.button-vector) {
    fill: var(--whitetext);
  }
  .button:active .button-vector-fill :global(.button-vector) {
    fill: var(--specialcolor);
  }
  .button {
    display:flex;
    align-items: center;
    flex-direction: row;
    gap: 10px;
    width: fit-content;
    justify-content: space-around;
  }
  .button-label {
    margin: 0;
    padding: 0;
    font-family: 'Lexend Deca', sans-serif;
    font-weight: 400;
    color: var(--darkcontroltext);
    text-align: center;
  }
</style>