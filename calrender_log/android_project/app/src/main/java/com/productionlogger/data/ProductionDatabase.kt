package com.productionlogger.data

import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
import android.content.Context

/**
 * Room 데이터베이스 클래스
 * SQLite 데이터베이스를 관리합니다.
 */
@Database(
    entities = [ProductionRecord::class, ModelInfo::class],
    version = 1,
    exportSchema = false
)
abstract class ProductionDatabase : RoomDatabase() {
    
    abstract fun productionDao(): ProductionDao
    
    companion object {
        @Volatile
        private var INSTANCE: ProductionDatabase? = null
        
        fun getDatabase(context: Context): ProductionDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    ProductionDatabase::class.java,
                    "production_database"
                )
                .fallbackToDestructiveMigration()
                .build()
                INSTANCE = instance
                instance
            }
        }
    }
}
