package com.productionlogger.data

import androidx.room.*
import kotlinx.coroutines.flow.Flow

/**
 * 생산 기록 데이터베이스 접근 객체
 * Room을 사용하여 데이터베이스 작업을 수행합니다.
 */
@Dao
interface ProductionDao {
    
    // 생산 기록 관련 쿼리
    @Query("SELECT * FROM production_records ORDER BY date DESC, createdAt DESC")
    fun getAllRecords(): Flow<List<ProductionRecord>>
    
    @Query("SELECT * FROM production_records WHERE date = :date ORDER BY createdAt DESC")
    fun getRecordsByDate(date: String): Flow<List<ProductionRecord>>
    
    @Query("SELECT * FROM production_records WHERE date >= :startDate AND date <= :endDate ORDER BY date DESC, createdAt DESC")
    fun getRecordsByDateRange(startDate: String, endDate: String): Flow<List<ProductionRecord>>
    
    @Query("SELECT * FROM production_records WHERE date >= :startDate AND date < :endDate ORDER BY date")
    fun getRecordsByMonth(startDate: String, endDate: String): Flow<List<ProductionRecord>>
    
    @Insert
    suspend fun insertRecord(record: ProductionRecord)
    
    @Update
    suspend fun updateRecord(record: ProductionRecord)
    
    @Delete
    suspend fun deleteRecord(record: ProductionRecord)
    
    // 모델 정보 관련 쿼리
    @Query("SELECT * FROM model_info ORDER BY modelName")
    fun getAllModels(): Flow<List<ModelInfo>>
    
    @Query("SELECT * FROM model_info WHERE modelName = :modelName")
    suspend fun getModelByName(modelName: String): ModelInfo?
    
    @Insert
    suspend fun insertModel(model: ModelInfo)
    
    @Update
    suspend fun updateModel(model: ModelInfo)
    
    @Delete
    suspend fun deleteModel(model: ModelInfo)
    
    // 통계 쿼리
    @Query("""
        SELECT 
            model,
            SUM(quantity) as totalQuantity,
            SUM(amount) as totalAmount,
            COUNT(*) as recordCount
        FROM production_records 
        WHERE date >= :startDate AND date < :endDate
        GROUP BY model
        ORDER BY totalQuantity DESC
    """)
    fun getModelStatistics(startDate: String, endDate: String): Flow<List<ModelStatistics>>
    
    @Query("""
        SELECT 
            date,
            SUM(quantity) as dailyQuantity,
            SUM(amount) as dailyAmount
        FROM production_records 
        WHERE date >= :startDate AND date < :endDate
        GROUP BY date
        ORDER BY date
    """)
    fun getDailyStatistics(startDate: String, endDate: String): Flow<List<DailyStatistics>>
}

/**
 * 모델별 통계 데이터 클래스
 */
data class ModelStatistics(
    val model: String,
    val totalQuantity: Int,
    val totalAmount: Int,
    val recordCount: Int
)

/**
 * 일별 통계 데이터 클래스
 */
data class DailyStatistics(
    val date: String,
    val dailyQuantity: Int,
    val dailyAmount: Int
)
