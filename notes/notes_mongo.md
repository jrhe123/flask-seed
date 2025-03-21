1. basic

db.students.find({})

```
db.students.findOne(
  {
    age: {
      $gte: 12,
      $lte: 18,
    },
  },
  {
    "stu_no": 1,
    "stu_nanme": 1,
    "address": 1,
    "_id": 0,
  }
)
```


2. filter
```
{
  age: {
    $gte: 12,
    $lte: 18,
  },
},
```

{ age: null },

{ age: {$ne: null} },

{ age: {$in: [12, 13, 14]} },

========

- $eq
- $ne
- $gt
- $gte
- $lt
- $lte
- $in
- $nin

```
{
  $or: [
    {sex: "male", age:{$gt: 12}},
    {sex: "female", age:{$lt: 18}},
  ]
},
```

========

$and
$not
$or
$nor

{
  "stu_name": /^roy$/
},

{
  "stu_name": /roy/
},

regex

========

```
db.grades.find({
  "grade.course_name": "cs"
})

db.grades.find({
  $and: [
    "grade.course_name": "cs",
    "grade.score": {
      $gte: 60
    },
  ]
})
```

embed search

========

$all
$elemMatch
$size

```
db.students.find({
  grades: {
    $size: 2
  }
})
```

embed search array

========

db.students.count()
db.students.distinct(stu_name, {})

methods:
count
distinct



3. aggregate

```
db.students.aggregate(
  [
    <!-- where -->
    {
      $match: {
        "grade.score": { $gte: 60 }
      }
    },
    <!-- grounp by -->
    {
      $group: {
        _id: "$stu_no",
        total: { $sum: 1 }
      }
    },
    <!-- having -->
    {
      $match: {$total: {$eq: 3}}
    }
  ]
)
```

========

func:

$sum
$avg
$min
$max
$first
$last

```
db.grades.aggregate(
  [
    <!-- where -->
    {
      $match: {
        "grade.course_name": "cs",
      }
    },
    <!-- group by -->
    {
      $group: {
        _id: null,
        maxScore: {
          $max: "$grade.score"
        },
        minScore: {
          $min: "$grade.score"
        },
        avgScore: {
          $avg: "$grade.score"
        }
      }
    }
  ]
)
```

```
db.grades.aggregate(
  [
    <!-- where -->
    {
      $match: {
        "stu_name": "roytest",
      }
    },
    <!-- group by -->
    {
      $group: {
        _id: null,
        totalScore: {
          $sum: "$grade.score"
        },
      }
    }
  ]
)
```

```
db.grades.aggregate(
  [
    <!-- group by -->
    {
      $group: {
        _id: "$class_name",
        totalStudent: { $sum: 1 },
      }
    }
  ]
)
```

```
db.grades.aggregate(
  [
    <!-- group by -->
    {
      $group: {
        _id: {
          class_name: "$class_name",
          sex: "$sex"
        },
        total: { $sum: 1 },
      }
    }
  ]
)
```

```
db.grades.aggregate(
  [
    <!-- where -->
    {
      $match: {
        "grade.score": {
          $gte: 60
        },
      }
    },
    <!-- group by -->
    {
      $group: {
        _id: "$stu_no",
        total: { $sum: 1 },
      }
    },
    <!-- having -->
    {
      $match: {
        total: {
          $eq: 3
        }
      }
    }
  ]
)
```

4. Pagination


descending

```
db.grades.find({
  "grade.course_name": "cs"
}).sort({
  "age": -1,
  "grade.score": -1
})

db.grades.find({}).skip(20).limit(10)
```


5. advanced search keyword:

- aggregate
- search
- compound
- must
- text
- query
- fuzzy
- maxEdit
- should
- autocomplete
- path
- minimumShouldMatch
- range
- filter
- skip
- limit
- type
- searchAnalyzer
- analyzer
- lucene.keyword


6. update

- updateOne()
- replaceOne()
- updateMany()

- $set
- $unset
- $currentDate
- $inc
- $min
- $max
- $mul
- $rename

```
db.students.updateMany(
  {},
  {
    $set: {
      age: 20
    }
  }
)

db.students.updateMany(
  {},
  {
    $unset: {
      company: null,
      hobby: null
    }
  }
)

db.students.updateMany(
  {},
  {
    $currentDate: {
      created_at: true,
    }
  }
)
```


7. delete

deleteMany()
deleteOne()

db.students.deleteMany({})
