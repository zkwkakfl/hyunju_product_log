package com.productionlogger.data

import androidx.room.Entity
import androidx.room.PrimaryKey
import java.util.Date

/**
 * 생산 기록 데이터 클래스
 * Room 데이터베이스의 엔티티로 사용됩니다.
 */
@Entity(tableName = "production_records")
data class ProductionRecord(
    @PrimaryKey(autoGenerate = true)
    val id: Int = 0,
    val date: String,           // 날짜 (YYYY-MM-DD 형식)
    val model: String,          // 모델명
    val quantity: Int,          // 수량
    val unitPrice: Int,         // 단가
    val amount: Int,            // 총 금액
    val createdAt: Long = System.currentTimeMillis()  // 생성 시간
)
