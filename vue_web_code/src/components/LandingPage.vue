<template>
  <section class="section">
    <h1>Omgevingsmanager beheerpagina</h1>

    <b-field
      class="align-left"
      label="Selecteer omgevings-manager of voeg een nieuwe toe.">
      <b-autocomplete
        ref="autocomplete"
        v-model="name"
        :keep-first="true"
        :open-on-focus="true"
        :data="filteredDataObj"
        :clearable="true"
        placeholder="e.g. p.veldhoven@amsterdam.nl"
        field="email"
        @select="option => (selected_project_manager = option)">
        <template #header>
          <a @click="showAddPM">
            <span> Voeg toe... </span>
          </a>
        </template>
        <template #empty>Geen resultaat voor {{ name }}</template>
      </b-autocomplete>
    </b-field>

    <b-field
      v-if="selected_project_manager != null">
      <b-table
        :data="projects"
        :columns="project_columns"
        :checked-rows.sync="selected_projects"
        :checkbox-position="checkboxPosition"
        :sticky-header="true"
        striped
        class="align-left"
        checkable>
        <template #bottom-left>
          <b>Totaal geselecteerd</b>: {{ selected_projects.length }} van {{ projects.length }}
        </template>
      </b-table>
    </b-field>
  </section>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      name: '',
      selected: null,
      selected_project_manager: null,
      project_managers: [],
      selected_projects: [],
      projects: [],
      project_columns: [
        {
          field: 'title',
          label: 'Project',
          sortable: true,
          searchable: true
        },
        {
          field: 'district_name',
          label: 'Locatie',
          sortable: true,
          searchable: true
        },
        {
          field: 'project_type',
          label: 'Type',
          sortable: true,
          searchable: true
        }
      ],
      checkboxPosition: 'left'
    }
  },
  computed: {
    filteredDataObj () {
      return this.project_managers.filter(option => {
        return (
          option.email
            .toString()
            .toLowerCase()
            .indexOf(this.name.toLowerCase()) >= 0
        )
      })
    }
  },
  watch: {
    selected_project_manager: {
      handler () {
        this.selected_projects = []
        for (let index in this.projects) {
          if (this.selected_project_manager.projects.includes(this.projects[index].identifier)) {
            this.selected_projects.push(this.projects[index])
          }
        }
      },
      deep: true
    }
  },
  created () {
    this.init()
  },
  methods: {
    init: function () {
      // Get current project_managers
      axios({methods: 'GET', 'url': '/project/manager'}).then(response => {
        this.project_managers = response.data.result
      }, error => {
        console.log(error)
      })

      // get current projects
      axios({methods: 'GET', 'url': '/projects'}).then(response => {
        this.projects = response.data.result
      }, error => {
        console.log(error)
      })
    },
    showAddPM () {
      this.$buefy.dialog.prompt({
        message: `Voer het email adres in`,
        inputAttrs: {
          placeholder: 'e.g. p.veldhoven@amsterdam.nl',
          maxlength: 50,
          value: this.name
        },
        confirmText: 'Toevoegen',
        cancelText: 'Afbreken',
        trapFocus: true,
        onConfirm: (value) => {
          let data = {email: value, projects: []}
          this.project_managers.push(data)
          this.$refs.autocomplete.setSelected(value)
          this.selected_project_manager = data
        }
      })
    }
  }
}
</script>

<style>
.align-left {
  text-align: left;
}

section {
  margin: 25px;
  height: 100vh;
  background: rgba(255,255,255,1.0);
}
</style>
