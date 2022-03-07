<template>
    <v-toolbar color="secondary" dense dark>
        <v-toolbar-title>{{ title }}</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn-toggle
            v-model="active_tool_id"
            class="transparent"
            borderless
            color="secondary"
            >
            <v-tooltip
                v-for="[id, {tooltip, icon}] of Object.entries(tools_data)"
                :key="id"
                top>
                <template v-slot:activator="{ on }">
                    <v-btn v-on="on" icon :value="id">
                        <v-icon>{{ icon }}</v-icon>
                    </v-btn>
                </template>
                <span>{{ tooltip }}</span>
            </v-tooltip>
        </v-btn-toggle>
    </v-toolbar>
</template>
