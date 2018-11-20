<template>
  <section>
    <b-field>
      <b-upload v-model="dropFiles"
                multiple
                drag-drop>
        <section class="section">
          <div class="content has-text-centered">
            <p>
              <span class="icon">
                  <i class="fas fa-arrow-circle-up fa-2x" aria-hidden="true"></i>
                </span>
            </p>
            <p>Drop your files here or click to upload</p>
          </div>
        </section>
      </b-upload>
    </b-field>

    <div class="columns">
        <div class="column">
            <div class="tags is-centered">
                <span v-for="(file, index) in dropFiles"
                      :key="index"
                      class="tag is-primary" >
                    {{file.name}}
                    <button class="delete is-small"
                            type="button"
                            @click="deleteDropFile(index)">
                    </button>
                </span>
            </div>
            <span class="is-centered" v-if="dropFiles.length === 1">
                <button class="button" style="margin-right: 12.25px" @click="doUpload">Upload</button>

            </span>

            <div class="card-body">
                <div class="messages">
                    <p><span class="font-weight-bold">{{ message }} </span></p>
                </div>
            </div>


            <span class="is-centered" v-if=" finished  === true">
                <a href="url"> {{link}}}</a>
                <!--<button class="button" style="margin-right: 12.25px" @click="">Download</button>-->

            </span>

        </div>

    </div>

  </section>
</template>

<!--<template>-->
    <!--<div class="card mt-3">-->
        <!--<div class="card-body">-->
            <!--<div class="card-title">-->
                <!--<h3>Chat Group</h3>-->
                <!--<hr>-->
            <!--</div>-->
            <!--<div class="card-body">-->
                <!--<div class="messages">-->

                <!--</div>-->
            <!--</div>-->
        <!--</div>-->
        <!--<div class="card-footer">-->
            <!--<form @submit.prevent="sendMessage">-->
                <!--<div class="gorm-group">-->
                    <!--<label for="user">User:</label>-->
                    <!--<input type="text" v-model="user" class="form-control">-->
                <!--</div>-->
                <!--<div class="gorm-group pb-3">-->
                    <!--<label for="message">Message:</label>-->
                    <!--<input type="text" v-model="message" class="form-control">-->
                <!--</div>-->
                <!--<button type="submit" class="btn btn-success">Send</button>-->
            <!--</form>-->
        <!--</div>-->
    <!--</div>-->
<!--</template>-->

<script>
    import axios from 'axios';

    export default {
        data() {
            return {
                dropFiles: [],
                uploaded: false,
                uuid:'DEFAULT UUID',
                status:'',
                isConnected: false,
                message:'',
                messages:[],
                socket : null,
                finished: false,
                downloadLink: '',

            }
        },
        methods: {
            deleteDropFile(index) {
                this.dropFiles.splice(index, 1)
                this.uploaded = false
            },
            doUpload(){
                // Todo: axios upload here

                axios.put("http://localhost:5555/upload",this.dropFiles[0]).then(res=> {
                    var json = JSON.parse(res.data);
                    this.uuid = json.uuid
                    this.uploaded = true
                    alert("upload completed")

                }).then(()=> {
                    console.log(this.uuid)
                    this.$router.push({
                    name: 'download',
                    params: {
                        uuid: this.uuid
                    }
                })})

            },
        },
    }
</script>

