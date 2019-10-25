<template>
    <svg viewBox="-200, -200, 400, 400">
        <g id="links">
            <path v-for="link in graph.links" :key="link.id" :d="`M ${link.source.x},${link.source.y} ${link.target.x},${link.target.y}`"/>
        </g>
        <g id="nodes">
            <circle v-for="node in graph.nodes" :key="node.id" :x="node.x" :y="node.y" :r="node.radius"/>
        </g>
    </svg>
</template>

