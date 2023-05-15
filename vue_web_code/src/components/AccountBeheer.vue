<template>
  <section class="section">
    <h1 class="align-left">Accountbeheer</h1>

    <b-field
      class="align-left">
      <span
        style="font-weight: 600; color: darkgray">
        Selecteer een bestaand account of voeg een account toe.
      </span>
    </b-field>
    <b-field
      class="align-left">
      <b-autocomplete
        ref="autocomplete"
        v-model="name"
        :keep-first="true"
        :open-on-focus="true"
        :data="filteredDataObj"
        :clearable="true"
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
        icon-pack="fas"
        striped
        class="align-left"
        checkable>
        <template #bottom-left>
          <b>Totaal geselecteerd</b>: {{ selected_projects.length }} van {{ projects.length }}
        </template>
      </b-table>
    </b-field>

    <b-field
      v-if="selected_project_manager != null"
      class="align-left">
      <b-button
        class="is-primary"
        @click="save()">
        <span style="font-weight: 600;">Bijwerken / Opslaan</span>
      </b-button>

      <b-button
        class="is-danger has-padding"
        @click="remove()">
        <span style="font-weight: 600;">Verwijderen</span>
      </b-button>
    </b-field>
  </section>
</template>

<script>
import axios from 'axios'
import jsPDF from 'jspdf'

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
        for (let i = 0; i < this.projects.length; i++) {
          if (this.projects[i].hasOwnProperty('identifier') && this.selected_project_manager !== null) {
            if (this.selected_project_manager.projects.includes(this.projects[i].identifier)) {
              this.selected_projects.push(this.projects[i])
            }
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
      axios({
        methods: 'GET',
        url: '/projects?page_size=10000',
        headers: {deviceid: '00000000-0000-0000-0000-000000000000'}}).then(response => {
        this.projects = response.data.result
      }, error => {
        console.log(error)
      })
    },
    showAddPM () {
      this.$buefy.dialog.prompt({
        title: 'Account toevoegen',
        message: 'Voer een geldig "@amsterdam.nl" email adres in.',
        inputAttrs: {
          type: 'text',
          maxlength: 50,
          value: this.name
        },
        confirmText: 'Toevoegen',
        cancelText: 'Afbreken',
        trapFocus: true,
        closeOnConfirm: false,
        onConfirm: (value, {close}) => {
          if (value.includes('@amsterdam.nl')) {
            let data = {email: value, projects: []}
            this.project_managers.push(data)
            this.$refs.autocomplete.setSelected(value)
            this.selected_project_manager = data
            close()
          } else {
            let message = '"' + value + '" is geen valide @amsterdam.nl adres'
            this.$buefy.toast.open(message)
          }
        }
      })
    },
    create_pdf (identifier) {
      // Generate PDF document for end user
      let name = this.selected_project_manager.email.split('@')[0]
      // eslint-disable-next-line new-cap
      let doc = new jsPDF()
      doc.setFont('helvetica')
      doc.setFontSize(8)
      let text = 'Geachte ' + name + ',\n\n'
      text += 'Uw account is geactiveerd voor de volgende projecten:\n\n'

      for (let item in this.selected_projects) {
        text += ' - ' + this.selected_projects[item].title + '\n'
      }

      text += '\n\nOpen de onderstaande link op uw telefoon om uw app te activeren\n\n'
      text += 'Met vriendelijke groet,\n\n'
      text += 'webredactie@amsterdam.nl\n\n---\n\n\n\n'
      doc.text(text, 10, 10)

      let lines = text.split('\n').length
      let lineHeight = doc.getLineHeight(text) / doc.internal.scaleFactor
      let textY = lines * lineHeight

      doc.text('https://api-backend.app-amsterdam.nl/omgevingsmanager/' + identifier, 10, textY)
      doc.save(name + '.pdf')
    },
    save () {
      let message = '<h1 style="padding-top:10px;padding-bottom:10px;">U staat op het punt om het account voor <b>' + this.selected_project_manager.email + '</b> toe te voegen / bij te werken.</h1>'
      message += '<div style="margin-bottom: 15px;"><p>U heeft de onderstaande projecten geselecteerd:</p></div>'

      // Updated selected projects for the selected project-manager
      this.selected_project_manager.projects = []
      message += '<div><ul>'
      for (let i = 0; i < this.selected_projects.length; i++) {
        this.selected_project_manager.projects.push(this.selected_projects[i].identifier)
        message += '<li><b> &middot; ' + this.selected_projects[i].title + '</b></li>'
      }
      message += '</ul></div>'
      let projectManager = this.selected_project_manager

      this.$buefy.dialog.confirm({
        title: 'Account bijwerken / opslaan',
        message: message,
        confirmText: 'Bijwerken / Opslaan',
        cancelText: 'Afbreken',
        type: 'is-primary',
        hasIcon: true,
        onConfirm: () => {
          axios.patch('/project/manager', projectManager).then(response => {
            if (response.data.hasOwnProperty('identifier')) {
              this.create_pdf(response.data.identifier)
              this.$buefy.toast.open('Account toegevoegd!')
            } else {
              this.$buefy.toast.open('Account bijgewerkt!')
            }

            // reload accounts and projects
            this.init()
            this.name = ''
            this.selected_projects = []
            this.selected_project_manager = null
          }, error => {
            console.log(error)
          })
        }
      })
    },
    remove () {
      let message = '<h1 style="padding-top:10px;padding-bottom:10px;">U staat op het punt om het account voor <b>' + this.selected_project_manager.email + '</b> te verwijderen. Deze actie kan niet ongedaan gemaakt worden.</h1>'
      message += '<p>Weet u zeker dat u dit account wilt <b>verwijderen?</b></p>'
      this.$buefy.dialog.confirm({
        title: 'Account verwijderen',
        message: message,
        confirmText: 'Verwijder account',
        cancelText: 'Afbreken',
        type: 'is-danger',
        hasIcon: true,
        onConfirm: () => {
          axios.delete('/project/manager', {params: {'id': this.selected_project_manager.identifier}}).then(response => {
            // reload accounts and projects
            this.init()
            this.name = ''
            this.selected_project_manager = null
            this.$buefy.toast.open('Account verwijderd!')
          }, error => {
            console.log(error)
          })
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

.has-padding {
  margin-left: 15px;
}

section {
  margin: 25px;
  height: 100vh;
  background: rgba(255,255,255,1.0);
}
</style>
