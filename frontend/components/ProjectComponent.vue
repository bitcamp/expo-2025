<template>
    <div class="entire-container">
        <div class="top-row">
            <div class="row-header">Table</div>
            <div class="row-header">Project</div>
        </div>
        <div class="content-row">
        </div>
        <div class="bottom-row">
        </div>
    </div>
</template>

<script setup lang="ts">

</script>

<style lang="scss">
.entire-container {
    background-color: #F6EBCC;
    border-radius: 3rem;
}

.top-row,
.bottom-row {
    height: 5rem;
    display: flex;
    flex-direction: row;
    padding: 1rem;
}

.row-header {
    font-size: 1.5rem;
    margin-inline: 1rem;
}
</style>