<template>
  <div
    v-if="edit === false"
    class="outer-section">
    <section>
      <h1 class="align-left">Berichtenbeheer</h1>
      <b-field class="align-left">
        <b-table
          ref="table"
          :data="warnings"
          :show-detail-icon="showDetailIcon"
          :sticky-header="true"
          :selected.sync="selected"
          sort-icon="chevron-up"
          sort-icon-size="is-medium"
          detail-transition="fade"
          icon-pack="fas"
          height="60vh"
          paginated
          pagination-simple="true"
          per-page="7"
          striped
          scrollable
          detailed
          detail-key="identifier"
          aria-page-label="Page"
          aria-current-label="Current page">

          <b-table-column
            v-slot="props"
            field="author_email"
            label="Auteur"
            width="21%"
            sortable
            searchable>
            {{ props.row.author_email }}
          </b-table-column>

          <b-table-column
            v-slot="props"
            field="project_title"
            label="Project"
            width="41%"
            sortable
            searchable>
            {{ props.row.project_title }}
          </b-table-column>

          <b-table-column
            v-slot="props"
            :custom-sort="sortByDate"
            field="date"
            label="Datum"
            width="10%"
            sortable
            searchable>
            {{ props.row.date }}
          </b-table-column>

          <b-table-column
            v-slot="props"
            width="14%">
            <b-button
              v-if="selectedIdentifier === props.row.identifier"
              size="is-small"
              type="is-primary"
              icon-pack="fas"
              icon-right="pen-square"
              @click="editor()">
              <span style="font-weight: 600;">Bewerken</span>
            </b-button>
            <div v-else>&nbsp;</div>
          </b-table-column>

          <b-table-column
            v-slot="props"
            width="14%">
            <b-button
              v-if="selectedIdentifier === props.row.identifier"
              size="is-small"
              type="is-danger"
              icon-pack="fas"
              icon-right="trash-alt"
              @click="remove()">
              <span style="font-weight: 600;">Verwijderen</span>
            </b-button>
            <div v-else>&nbsp;</div>
          </b-table-column>

          <template #detail="props">
            <article class="media">
              <div class="media-content">
                <div class="content">
                  <p>
                    <span style="color: darkgray">{{ props.row.project_title }}</span>
                    <br>
                    <strong>{{ props.row.title }}</strong>
                  </p>
                  <p>
                    <strong>Inleiding</strong>
                    <br>
                    {{ props.row.body.preface }}
                  </p>
                  <p>
                    <strong>Bericht tekst</strong>
                    <br>
                    {{ props.row.body.content }}
                  </p>
                </div>
              </div>
            </article>
          </template>
        </b-table>
      </b-field>
    </section>
  </div>

  <div
    v-else
    class="outer-section">
    <section>
      <h1 class="align-left">Bericht bewerken</h1>

      <div
        class="align-left margin-less">
        <span
          style="font-weight: 600; color: darkgray">
          titel
        </span>
      </div>
      <b-field class="align-left">
        <b-input
          v-model="title"/>
      </b-field>

      <div class="spacer"/>

      <div
        class="align-left margin-less">
        <span
          style="font-weight: 600; color: darkgray">
          Inleiding
        </span>
      </div>
      <b-field class="align-left">
        <b-input
          v-model="preface"
          maxlength="4000"
          type="textarea"/>
      </b-field>

      <div
        class="align-left margin-less">
        <span
          style="font-weight: 600; color: darkgray">
          Bericht tekst
        </span>
      </div>
      <b-field class="align-left">
        <b-input
          v-model="content"
          maxlength="4000"
          type="textarea"/>
      </b-field>

      <b-field
        class="align-left">
        <b-button
          class="is-primary"
          @click="edit = false">
          <span style="font-weight: 600;">Afbreken</span>
        </b-button>

        <b-button
          class="is-danger has-padding"
          @click="save()">
          <span style="font-weight: 600;">Opslaan</span>
        </b-button>
      </b-field>
    </section>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    let warnings = []
    return {
      edit: false,
      selected: warnings[0],
      selectedIdentifier: 0,
      title: '',
      preface: '',
      content: '',
      identifier: '',
      showDetailIcon: true,
      useTransition: true,
      warnings
    }
  },
  computed: {
    transitionName () {
      if (this.useTransition) {
        return 'fade'
      }
    }
  },
  watch: {
    selected: {
      handler () {
        this.selectedIdentifier = this.selected.identifier
      }
    },
    warnings: {
      handler () {
        this.selected = this.warnings[0]
      }
    }
  },
  created () {
    this.init()
  },
  methods: {
    init: function () {
      // Get current project_managers
      axios({methods: 'GET', 'url': '/project/warnings'}).then(response => {
        let warningResponse = response.data.result

        axios({
          methods: 'GET',
          url: '/projects',
          headers: {deviceid: '00000000-0000-0000-0000-000000000000'}}).then(response => {
          let titles = {}
          for (let i = 0; i < response.data.result.length; i++) {
            titles[response.data.result[i].identifier] = response.data.result[i].title
          }
          for (let i = 0; i < warningResponse.length; i++) {
            warningResponse[i]['project_title'] = titles[warningResponse[i]['project_identifier']]
            warningResponse[i]['date'] = warningResponse[i]['modification_date'].split('T')[0]
          }

          this.warnings = warningResponse.sort(function (a, b) { return new Date(b.modification_date) - new Date(a.modification_date) })
        })
      }, error => {
        console.log(error)
      })
    },
    sortByDate (a, b, isAsc) {
      let firstArgument = new Date(a.modification_date).getTime()
      let secondArgument = new Date(b.modification_date).getTime()
      if (isAsc) {
        return secondArgument - firstArgument
      } else {
        return firstArgument - secondArgument
      }
    },
    editor: function () {
      this.title = this.selected.title
      this.preface = this.selected.body.preface
      this.content = this.selected.body.content
      this.identifier = this.selectedIdentifier
      this.edit = true
    },
    remove () {
      let message = '<h1 style="padding-top:10px;padding-bottom:10px;">U staat op het punt om onderstaande bericht te <b>verwijderen</b>. Deze actie kan niet ongedaan gemaakt worden.</h1>'
      message += '<div class="content">\n' +
          '                  <p>\n' +
          '                    <span style="color: darkgray">' + this.selected.title + '</span>\n' +
          '                  </p>\n' +
          '                  <p>\n' +
          '                    <strong>Inleiding</strong>\n' +
          '                    <br>\n' +
          this.selected.body.preface +
          '                  </p>\n' +
          '                  <p>\n' +
          '                    <strong>Bericht tekst</strong>\n' +
          '                    <br>\n' +
          this.selected.body.content +
          '                  </p>\n' +
          '                </div>'
      this.$buefy.dialog.confirm({
        title: 'Bericht verwijderen',
        message: message,
        confirmText: 'Verwijder bericht',
        cancelText: 'Afbreken',
        type: 'is-danger',
        hasIcon: false,
        onConfirm: () => {
          axios.delete('/project/warning', {params: {'id': this.selected.identifier}}).then(response => {
            // reload warning messages
            const index = this.warnings.findIndex(warning => warning.identifier === this.selected.identifier)
            if (~index) { this.warnings.splice(index, 1) }
            this.$buefy.toast.open('Bericht verwijderd!')
          }, error => {
            console.log(error)
          })
        }
      })
    },
    save () {
      this.edit = false
      let payload = {
        identifier: this.identifier,
        title: this.title,
        body: {
          preface: this.preface,
          content: this.content
        }
      }
      axios.patch('/project/warning', payload).then(response => {
        this.$buefy.toast.open('Wijzigingen zijn opgeslagen')
        this.init()
        this.selected = []
      }, error => {
        console.log(error)
      })
    }
  }
}
</script>

<style>
.align-left {
  text-align: left;
}

.outer-section {
  margin: 125px;
  background: rgba(255,255,255,1.0);
}

.margin-less {
  margin: 0;
  padding: 0;
}

.spacer {
  margin: 30px;
}

section {
  margin: 25px;
}

</style>
