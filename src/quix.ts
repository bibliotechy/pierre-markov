import {WorkerHttpvfs} from "sql.js-httpvfs"


interface KeysQueryResult {
  KEY: string;
}

interface ValueAndCountQueryResult {
  VALUE: string;
  COUNT: number;
}

interface ChapterQueryResult {
  CHAPTER: string;
}

export class QuixSql {
  worker: WorkerHttpvfs;
  _fragment: string = "";
  _currentKey?: string;
  _values: ValueAndCountQueryResult[] =[];
  _chapter?: string = "";
  _finalFragment: Boolean


  constructor(worker: WorkerHttpvfs) {
    this.worker = worker;
    this.randomKey()
      .then((key) => {
        this._fragment = key
        this._currentKey = key
      })
    this.values().then(() => console.log("constructor values are", this._values))
    this._finalFragment = false;

  }

    // def __init__(this, :):
    //     this.db = sqlite3.connect(db_path).cursor()
    //     this._fragment = this.randomKey()
    //     this._currentKey = this._fragment
    //     this._values = None
    //     this._chapter = None

    
   async generate_fragment() {
        var lc = 0
        debugger
        while ((!this._finalFragment) && ((await this.values()).length) > 0){
            lc += 1;
            console.log(lc)
            const randomIndex = Math.floor( Math.random() * this.values.length)
            const next_word = (await this.values()).splice(randomIndex, 1)[0].VALUE
            const possible_next_fragment = [this.fragment(), next_word].join(" ")
            if (await this.fragment_chapter(possible_next_fragment))
            {
                this._fragment = possible_next_fragment
                this._currentKey = undefined
                this._values = []
                this.generate_fragment()
            }
            else {
              continue
            }
          }
              
        this._finalFragment = true

        return {"fragment": this.fragment(), "chapter": (await this.fragment_chapter(this.fragment()) as string[])[0]}
      }

    fragment_chapter(fragment: string) {
        if (this._chapter) {
            return this.known_fragment_chapter(fragment)
        }
        return this.not_yet_known_fragment_chapter(fragment)
    }
    
    async not_yet_known_fragment_chapter(fragment: string) {
        const chapters =  await this.worker.db.query("SELECT chapter from chapters where text like ?", ["%"+fragment+"%"]) as string[]
        if (chapters.length === 1){
          this._chapter = chapters[0][0] 
        }
        return chapters ? chapters : undefined
      }
            

    async known_fragment_chapter(fragment: string) : Promise<string>  {
        const chapter = await this.worker.db.query("SELECT chapter from chapters where text like ? and chapter=?", [`%{fragment}%`, this._chapter]) as ChapterQueryResult[]
        return chapter[0].CHAPTER
    
    }

    async values() : Promise<ValueAndCountQueryResult[]> {
        if (this._values.length === 0) {
          this._values = await this.values_from(this.currentKey())
        }
        return this._values
      }

    currentKey() : string {
        if (this._currentKey === undefined) {
          const new_key_elements = this.fragment().split(' ')
          this._currentKey = new_key_elements.slice(new_key_elements.length -2).join(" ")
        }
          
        return this._currentKey
    }

    async randomKey() : Promise<string>{
        const key =  await this.worker.db.query("SELECT key from ENGLISH ORDER BY RANDOM() LIMIT 1") as KeysQueryResult[]
        return key[0].KEY
    }

    fragment(){
        return this._fragment
    }

    async values_from(key: string) : Promise<ValueAndCountQueryResult[]> {
        const values = await this.worker.db.query("SELECT value, count from ENGLISH where key=?", [key]) as ValueAndCountQueryResult[]
        return values
    }

    async random_value_from(key: string) : Promise<string> {
        const words_and_counts = await this.values_from(key)
        const weighted_words: string[] = words_and_counts.flatMap((value) => Array(value.COUNT).fill(value.VALUE))
        const randomIndex = Math.floor( Math.random() * weighted_words.length)
        return weighted_words[randomIndex]
    }

    async random_value_from_random() {
        return await this.random_value_from(await this.randomKey())
    }
  
}
